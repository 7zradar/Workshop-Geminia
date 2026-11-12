"""Pruebas reales, instantáneas e integridad de reportes del workshop."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WRITE_LOCK = threading.Lock()


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


@dataclass(frozen=True)
class Snapshot:
    source: bytes
    cases: bytes
    specification: str
    runner: bytes
    knowledge: tuple = ()  # pares (archivo, texto) de conocimiento/*.md

    @classmethod
    def capture(cls, root: Path = ROOT) -> Snapshot:
        folder = root / "conocimiento"
        knowledge = tuple((path.name, path.read_text(encoding="utf-8"))
                          for path in sorted(folder.glob("*.md"))) if folder.is_dir() else ()
        return cls(
            (root / "app/calculadora.mjs").read_bytes(),
            (root / "contratos/casos.json").read_bytes(),
            (root / "specs/aplicacion.md").read_text(encoding="utf-8"),
            (root / "scripts/ejecutar-pruebas.mjs").read_bytes(),
            knowledge,
        )

    @property
    def source_hash(self) -> str:
        return digest(self.source)

    @property
    def contract_hash(self) -> str:
        return digest(self.cases + self.specification.encode("utf-8") + self.runner)

    @property
    def knowledge_hash(self) -> str:
        return digest("\0".join(f"{name}\0{text}" for name, text in self.knowledge).encode("utf-8"))

    def identity(self, mode: str, model: str = "") -> str:
        base = f"{self.source_hash}:{self.contract_hash}:{mode}:{model}"
        if self.knowledge:  # Sin conocimiento la identidad es la de siempre.
            base += f":{self.knowledge_hash}"
        return digest(base.encode())[:20]


STOPWORDS = {"de", "la", "el", "los", "las", "un", "una", "y", "o", "en", "se", "al", "del", "por",
             "con", "para", "que", "es", "son", "no", "lo", "su", "sus", "hasta", "desde", "cada",
             "solo", "como", "mas", "ante", "sin", "sobre", "este", "esta"}
NUMBER_WORDS = {"diez": "10", "once": "11"}


def tokens(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", text.lower())
    words = re.findall(r"[a-z0-9]+", "".join(c for c in normalized if not unicodedata.combining(c)))
    stems = set()
    for word in words:
        word = NUMBER_WORDS.get(word, word)
        if word in STOPWORDS:
            continue
        if len(word) > 4 and word.endswith("es"):
            word = word[:-2]
        elif len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        stems.add(word)
    return stems


def knowledge_chunks(snapshot: Snapshot) -> list[dict]:
    """Divide cada documento en fragmentos por encabezado de segundo nivel."""
    chunks = []
    for name, text in snapshot.knowledge:
        title, body = None, []
        for line in text.splitlines() + ["## "]:
            if line.startswith("## "):
                if title and body:
                    chunks.append({"source": f"{name}#{title}", "title": title, "text": " ".join(body).strip()})
                title, body = line[3:].strip(), []
            elif title is not None and line.strip():
                body.append(line.strip())
    return chunks


def search_knowledge(snapshot: Snapshot, query: str, limit: int = 3) -> list[dict]:
    """Recuperación determinista por palabras clave. El título pesa el doble."""
    wanted = tokens(query)
    scored = []
    for chunk in knowledge_chunks(snapshot):
        score = len(wanted & tokens(chunk["text"])) + 2 * len(wanted & tokens(chunk["title"]))
        if score >= 2:
            scored.append((-score, chunk["source"], chunk))
    scored.sort(key=lambda item: item[:2])
    return [{"source": chunk["source"], "title": chunk["title"], "excerpt": chunk["text"][:400], "score": -negative}
            for negative, _, chunk in scored[:limit]]


def execute_tests(snapshot: Snapshot) -> dict:
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Node no está disponible. Instale Node 22 o superior.")
    with tempfile.TemporaryDirectory(prefix="workshop-qa-") as directory:
        folder = Path(directory)
        (folder / "calculadora.mjs").write_bytes(snapshot.source)
        (folder / "casos.json").write_bytes(snapshot.cases)
        (folder / "runner.mjs").write_bytes(snapshot.runner)
        process = subprocess.run(
            [node, str(folder / "runner.mjs"), "--motor", str(folder / "calculadora.mjs"),
             "--casos", str(folder / "casos.json")],
            capture_output=True, encoding="utf-8", timeout=30, check=False,
        )
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("El runner no produjo un resultado JSON válido.") from error
    if process.returncode not in (0, 1) or "tests" not in result:
        raise RuntimeError(result.get("error", "Falló la ejecución de las pruebas."))
    result["source_hash"] = snapshot.source_hash
    result["contract_hash"] = snapshot.contract_hash
    return result


class Evidence:
    """Las dos herramientas de una ejecución comparten la misma instantánea."""

    def __init__(self, snapshot: Snapshot):
        self.snapshot = snapshot
        self.result: dict | None = None
        self.trace: list[dict] = []
        self.citations: list[dict] = []

    def criteria(self) -> dict:
        self.trace.append({"actor": "qa", "event": "tool", "name": "leer_criterios"})
        return {"specification": self.snapshot.specification,
                "cases": json.loads(self.snapshot.cases),
                "contract_hash": self.snapshot.contract_hash}

    def context(self, query: str) -> dict:
        self.trace.append({"actor": "qa", "event": "tool", "name": "buscar_contexto"})
        results = search_knowledge(self.snapshot, query)
        known = {item["source"] for item in self.citations}
        self.citations += [{key: item[key] for key in ("source", "title", "excerpt")}
                           for item in results if item["source"] not in known]
        return {"query": query, "results": results}

    def tests(self) -> dict:
        self.trace.append({"actor": "qa", "event": "tool", "name": "ejecutar_pruebas"})
        if self.result is None:
            self.result = execute_tests(self.snapshot)
        return self.result


def local_analysis(result: dict, lookup=None) -> dict:
    """lookup(consulta) devuelve las fuentes de apoyo de un caso fallido."""
    failures = [test for test in result["tests"] if not test["passed"]]
    return {
        "summary": f"{result['summary']['passed']} de {result['summary']['total']} pruebas aprobadas. "
                   f"{len(failures)} diferencias frente a la especificación.",
        "findings": [
            {"case_id": test["id"], "description": f"{test['name']}. Se esperaba {test['expected']} "
             f"y se obtuvo {test['actual']}.",
             "recommendation": "Revisar la implementación frente al criterio de este caso y repetir la prueba.",
             "sources": lookup(f"{test['name']} {test['criterion']}") if lookup else []}
            for test in failures
        ],
        "next_action": "Corregir los casos fallidos y volver a ejecutar QA." if failures
                       else f"Conservar la evidencia. Los {result['summary']['total']} casos ejecutados cumplen sus criterios.",
    }


def validate_analysis(analysis: dict, result: dict, context: list[dict] | None = None) -> None:
    failed = {test["id"] for test in result["tests"] if not test["passed"]}
    ids = [finding["case_id"] for finding in analysis["findings"]]
    if set(ids) != failed or len(ids) != len(set(ids)):
        raise ValueError("El diagnóstico debe cubrir exactamente los casos fallidos, sin duplicados.")
    retrieved = {item["source"] for item in context or []}
    for finding in analysis["findings"]:
        invented = set(finding.get("sources", [])) - retrieved
        if invented:
            raise ValueError(f"Fuentes citadas que no se recuperaron en esta ejecución: {sorted(invented)}.")


def build_report(snapshot: Snapshot, result: dict, analysis: dict, review: dict,
                 trace: list[dict], mode: str, trigger: str, model: str = "",
                 context: list[dict] | None = None) -> dict:
    validate_analysis(analysis, result, context)
    return {
        "schema_version": 1,
        "id": snapshot.identity(mode, model),
        "executed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": mode, "model": model or None, "trigger": trigger,
        "source_hash": snapshot.source_hash, "contract_hash": snapshot.contract_hash,
        "verdict": "CON_FALLAS" if result["summary"]["failed"] else "SIN_FALLAS",
        "summary": result["summary"], "tests": result["tests"],
        "analysis": analysis, "review": review, "trace": trace,
        "context": context or [],
    }


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".qa-", suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def persist_report(report: dict, output: Path) -> None:
    with WRITE_LOCK:
        atomic_json(output / "reportes" / f"{report['id']}.json", report)
        atomic_json(output / "ultimo.json", report)


def read_history(output: Path) -> list[dict]:
    reports = []
    with WRITE_LOCK:
        for path in (output / "reportes").glob("*.json"):
            report = json.loads(path.read_text(encoding="utf-8"))
            reports.append({key: report[key] for key in (
                "id", "executed_at", "mode", "trigger", "source_hash", "verdict", "summary")})
    return sorted(reports, key=lambda report: report["executed_at"], reverse=True)
