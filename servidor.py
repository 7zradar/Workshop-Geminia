"""Servidor local del dashboard y disparador por cambios de código."""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import queue
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from procesar import run_pipeline
from qa_core import ROOT, Snapshot, read_history


def gemini_ready() -> bool:
    if os.getenv("GOOGLE_API_KEY"):
        return True
    try:
        from dotenv import dotenv_values
        return bool(dotenv_values(ROOT / ".env").get("GOOGLE_API_KEY"))
    except ImportError:
        return False


class Coordinator:
    def __init__(self, root: Path = ROOT, mode: str = "evidencia", watch: bool = True):
        self.root = root
        self.mode = mode
        self.watch = watch
        self.output = root / "salida"
        self.lock = threading.Lock()
        self.pending: set[str] = set()
        self.jobs: queue.Queue = queue.Queue()
        self.stop = threading.Event()
        self.last_seen = ""
        self.state = {"running": False, "error": None, "last_id": None}

    def start(self) -> None:
        threading.Thread(target=self._worker, daemon=True).start()
        threading.Thread(target=self._watcher, daemon=True).start()
        self.submit("inicio")

    def status(self) -> dict:
        with self.lock:
            return {**self.state, "mode": self.mode, "watch": self.watch,
                    "queued": len(self.pending), "gemini_ready": gemini_ready()}

    def submit(self, trigger: str, mode: str | None = None) -> bool:
        if mode is not None and mode not in ("evidencia", "gemini"):
            raise ValueError("Modo inválido.")
        snapshot = Snapshot.capture(self.root)
        with self.lock:
            selected = mode or self.mode
            if selected == "gemini" and not gemini_ready():
                raise ValueError("Configure GOOGLE_API_KEY en .env y reinicie la ejecución Gemini.")
            self.mode = selected
            identity = snapshot.identity(selected)
            self.last_seen = identity
            if identity in self.pending:
                return False
            self.pending.add(identity)
            self.state["error"] = None
            self.jobs.put((snapshot, selected, trigger, identity))
        return True

    def _worker(self) -> None:
        while not self.stop.is_set():
            try:
                snapshot, mode, trigger, identity = self.jobs.get(timeout=0.5)
            except queue.Empty:
                continue
            with self.lock:
                self.state["running"] = True
            try:
                report = run_pipeline(snapshot, mode, trigger, self.output)
                with self.lock:
                    self.state.update(last_id=report["id"], error=None)
            except Exception as error:
                message = (f"Gemini no completó la ejecución ({type(error).__name__}). "
                           "Revise la clave, el modelo, la cuota y la conexión.") if mode == "gemini" else str(error)
                with self.lock:
                    self.state["error"] = message
            finally:
                with self.lock:
                    self.pending.discard(identity)
                    self.state["running"] = False
                self.jobs.task_done()

    def _watcher(self) -> None:
        while not self.stop.wait(1):
            with self.lock:
                enabled, mode, last_seen = self.watch, self.mode, self.last_seen
            if not enabled:
                continue
            try:
                current = Snapshot.capture(self.root).identity(mode)
                if current != last_seen:
                    # Espera una escritura estable del editor antes de capturarla.
                    if self.stop.wait(0.3):
                        return
                    self.submit("cambio")
            except (OSError, ValueError) as error:
                with self.lock:
                    self.state["error"] = str(error)

    def apply_scenario(self, scenario: str) -> bool:
        choices = {"defectuosa": "version-con-error.mjs", "corregida": "version-corregida.mjs"}
        if scenario not in choices:
            raise ValueError("Escenario inválido.")
        target = self.root / "app/calculadora.mjs"
        content = (self.root / "demo" / choices[scenario]).read_bytes()
        if target.read_bytes() == content:
            return False
        descriptor, name = tempfile.mkstemp(dir=target.parent, suffix=".tmp")
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content)
            os.replace(name, target)
        finally:
            Path(name).unlink(missing_ok=True)
        with self.lock:
            enabled = self.watch
        if not enabled:
            self.submit("escenario")
        return True


def make_handler(coordinator: Coordinator):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def send_bytes(self, data: bytes, mime: str, status: int = 200):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def send_json(self, value: object, status: int = 200):
            self.send_bytes(json.dumps(value, ensure_ascii=False).encode(), "application/json; charset=utf-8", status)

        def do_GET(self):
            path = unquote(urlsplit(self.path).path)
            try:
                if path == "/":
                    self.send_response(302)
                    self.send_header("Location", "/pagina/index.html")
                    self.end_headers()
                    return
                if path == "/api/status":
                    return self.send_json(coordinator.status())
                if path == "/api/history":
                    return self.send_json(read_history(coordinator.output))
                if path == "/api/report":
                    latest = coordinator.output / "ultimo.json"
                    return self.send_json(json.loads(latest.read_text(encoding="utf-8"))) if latest.exists() else self.send_json(None)
                if path.startswith("/api/report/"):
                    identifier = path.removeprefix("/api/report/")
                    if len(identifier) != 20 or any(char not in "0123456789abcdef" for char in identifier):
                        raise ValueError("ID inválido.")
                    report = coordinator.output / "reportes" / f"{identifier}.json"
                    return self.send_json(json.loads(report.read_text(encoding="utf-8")))
                aliases = {"/": "pagina/index.html", "/presentacion": "WORKSHOP_GEMINI.html"}
                relative = aliases.get(path, path.lstrip("/"))
                if ".." in relative.replace("\\", "/").split("/"):
                    return self.send_json({"error": "Recurso no disponible."}, 404)
                allowed = relative in ("WORKSHOP_GEMINI.html", "app/calculadora.mjs") or relative.startswith(("pagina/", "presentacion/"))
                file = (coordinator.root / relative).resolve()
                if not allowed or not file.is_relative_to(coordinator.root.resolve()) or not file.is_file():
                    return self.send_json({"error": "Recurso no disponible."}, 404)
                mime = "text/javascript" if file.suffix in (".mjs", ".js") else mimetypes.guess_type(file.name)[0] or "application/octet-stream"
                self.send_bytes(file.read_bytes(), mime + "; charset=utf-8")
            except (ValueError, OSError, json.JSONDecodeError):
                self.send_json({"error": "No se pudo leer el recurso."}, 404)

        def do_POST(self):
            origin = self.headers.get("Origin")
            if origin and urlsplit(origin).netloc != self.headers.get("Host"):
                return self.send_json({"error": "Origen no permitido."}, 403)
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 <= length <= 4096:
                    raise ValueError("Solicitud demasiado grande.")
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise ValueError("Se esperaba un objeto JSON.")
                path = urlsplit(self.path).path
                if path == "/api/run":
                    coordinator.submit("manual", body.get("mode"))
                elif path == "/api/watch":
                    if not isinstance(body.get("enabled"), bool):
                        raise ValueError("enabled debe ser booleano.")
                    with coordinator.lock:
                        coordinator.watch = body["enabled"]
                elif path == "/api/scenario":
                    changed = coordinator.apply_scenario(body.get("name", ""))
                    return self.send_json({**coordinator.status(), "changed": changed}, 202)
                else:
                    return self.send_json({"error": "Acción no disponible."}, 404)
                self.send_json(coordinator.status(), 202)
            except (ValueError, TypeError, OSError) as error:
                self.send_json({"error": str(error)}, 400)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--mode", choices=["evidencia", "gemini"], default="evidencia")
    parser.add_argument("--no-watch", action="store_true")
    args = parser.parse_args()
    coordinator = Coordinator(mode=args.mode, watch=not args.no_watch)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(coordinator))
    coordinator.start()
    print(f"Dashboard http://127.0.0.1:{args.port}/", flush=True)
    print(f"Presentación http://127.0.0.1:{args.port}/presentacion", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        coordinator.stop.set()
        server.server_close()


if __name__ == "__main__":
    main()
