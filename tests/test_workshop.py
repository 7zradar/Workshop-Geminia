import json
import shutil
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

import pytest

from procesar import run_pipeline
from qa_core import ROOT, Snapshot, execute_tests, read_history, validate_analysis
from servidor import Coordinator, make_handler


def snapshot_version(name):
    current = Snapshot.capture()
    return Snapshot((ROOT / f"demo/version-{name}.mjs").read_bytes(), current.cases,
                    current.specification, current.runner)


@pytest.mark.parametrize("name,passed,failed", [("con-error", 2, 2), ("corregida", 4, 0)])
def test_real_runner(name, passed, failed):
    result = execute_tests(snapshot_version(name))
    assert result["summary"]["passed"] == passed
    assert result["summary"]["failed"] == failed
    case = next(item for item in result["tests"] if item["id"] == "QA-03")
    assert case["expected"] == 74
    assert case["actual"] == (99 if failed else 74)


def test_identity_keeps_contract_and_changes_source():
    bad, fixed = snapshot_version("con-error"), snapshot_version("corregida")
    assert bad.contract_hash == fixed.contract_hash
    assert bad.source_hash != fixed.source_hash
    assert bad.identity("evidencia") != bad.identity("gemini")


def test_repeat_replaces_report_without_duplicating_history(tmp_path):
    snapshot = snapshot_version("con-error")
    first = run_pipeline(snapshot, output=tmp_path)
    second = run_pipeline(snapshot, output=tmp_path)
    assert first["id"] == second["id"]
    assert len(read_history(tmp_path)) == 1
    assert json.loads((tmp_path / "ultimo.json").read_text(encoding="utf-8"))["id"] == second["id"]


def test_report_rejects_invented_findings():
    result = execute_tests(snapshot_version("corregida"))
    with pytest.raises(ValueError, match="casos fallidos"):
        validate_analysis({"findings": [{"case_id": "QA-03"}]}, result)


def test_failed_run_preserves_last_report(tmp_path):
    saved = run_pipeline(snapshot_version("corregida"), output=tmp_path)
    current = snapshot_version("con-error")
    broken = Snapshot(b"this is invalid javascript", current.cases, current.specification, current.runner)
    with pytest.raises(RuntimeError):
        run_pipeline(broken, output=tmp_path)
    assert json.loads((tmp_path / "ultimo.json").read_text())["id"] == saved["id"]


def test_missing_key_is_explicit(monkeypatch, tmp_path):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    import dotenv
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)
    with pytest.raises(RuntimeError, match="GOOGLE_API_KEY"):
        run_pipeline(snapshot_version("con-error"), mode="gemini", output=tmp_path)
    assert not (tmp_path / "ultimo.json").exists()


def make_workspace(tmp_path):
    for directory in ("app", "contratos", "specs", "scripts", "demo"):
        (tmp_path / directory).mkdir()
    for name in ("app/calculadora.mjs", "contratos/casos.json", "specs/aplicacion.md", "scripts/ejecutar-pruebas.mjs",
                 "demo/version-con-error.mjs", "demo/version-corregida.mjs"):
        shutil.copy2(ROOT / name, tmp_path / name)
    shutil.copy2(ROOT / "demo/version-con-error.mjs", tmp_path / "app/calculadora.mjs")
    return tmp_path


def wait_until(predicate, seconds=8):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if predicate():
            return
        time.sleep(0.05)
    raise AssertionError("La ejecución no alcanzó el estado esperado.")


def test_file_change_triggers_real_pipeline(tmp_path):
    coordinator = Coordinator(make_workspace(tmp_path))
    coordinator.start()
    try:
        wait_until(lambda: len(read_history(coordinator.output)) == 1)
        coordinator.apply_scenario("corregida")
        wait_until(lambda: len(read_history(coordinator.output)) == 2)
        report = json.loads((coordinator.output / "ultimo.json").read_text())
        assert report["trigger"] == "cambio"
        assert report["summary"]["passed"] == 4
        coordinator.apply_scenario("corregida")
        assert len(read_history(coordinator.output)) == 2
    finally:
        coordinator.stop.set()


def test_http_routes_keep_secrets_private(tmp_path):
    root = make_workspace(tmp_path)
    (root / ".env").write_text("GOOGLE_API_KEY=test-secret", encoding="utf-8")
    coordinator = Coordinator(root)
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(coordinator))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        for path in ("/.env", "/../.env", "/pagina/../.env", "/.git/config"):
            with pytest.raises(HTTPError) as failure:
                urlopen(base + path)
            assert failure.value.code == 404
        request = Request(base + "/api/run", data=b'{}', headers={"Origin": "https://example.org", "Content-Type": "application/json"})
        with pytest.raises(HTTPError) as failure:
            urlopen(request)
        assert failure.value.code == 403
        status = json.load(urlopen(base + "/api/status"))
        assert "test-secret" not in json.dumps(status)
    finally:
        server.shutdown()
        server.server_close()


def test_two_adk_agents_with_injected_model(monkeypatch, tmp_path):
    """Valida el runtime ADK con herramientas reales. El modelo de esta prueba es local."""
    from google.adk.models.base_llm import BaseLlm
    from google.adk.models.llm_response import LlmResponse
    from google.genai import types
    import flujo.agent as flow

    class LocalModel(BaseLlm):
        async def generate_content_async(self, llm_request, stream=False):
            if llm_request.config.response_schema:
                text = json.dumps({"decision": "VALIDADO", "observations": ["Evidencia revisada por el modelo de prueba local."]})
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))
                return
            calls = []
            for content in llm_request.contents:
                for part in content.parts or []:
                    if part.function_response:
                        calls.append(part.function_response.name)
            if "leer_criterios" not in calls:
                name = "leer_criterios"
            elif "ejecutar_pruebas" not in calls:
                name = "ejecutar_pruebas"
            else:
                text = json.dumps({"summary": "Dos pruebas fallidas.", "findings": [
                    {"case_id": identifier, "description": "Esperado y obtenido difieren.", "recommendation": "Corregir el cálculo."}
                    for identifier in ("QA-02", "QA-03")
                ], "next_action": "Corregir y repetir."})
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))
                return
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=name, args={}))]))

    original = flow.create_pipeline
    monkeypatch.setattr(flow, "create_pipeline", lambda evidence, model: original(evidence, LocalModel(model="modelo-local-de-prueba")))
    monkeypatch.setenv("GOOGLE_API_KEY", "clave-ficticia-solo-para-el-test")
    report = run_pipeline(snapshot_version("con-error"), mode="gemini", output=tmp_path)
    assert report["summary"]["failed"] == 2
    assert report["review"]["decision"] == "VALIDADO"
    assert {event["actor"] for event in report["trace"]} >= {"agente_qa", "revisor_qa"}
    assert {event["name"] for event in report["trace"]} >= {"leer_criterios", "ejecutar_pruebas"}


def test_adk_chat_captures_new_source_each_turn(monkeypatch):
    from types import SimpleNamespace
    from agente.agent import create_agent

    context = SimpleNamespace(state={})
    agent = create_agent()
    bad = Snapshot((ROOT / "demo/version-con-error.mjs").read_bytes(),
                   (ROOT / "contratos/casos.json").read_bytes(),
                   (ROOT / "specs/aplicacion.md").read_text(encoding="utf-8"),
                   (ROOT / "scripts/ejecutar-pruebas.mjs").read_bytes())
    fixed = Snapshot((ROOT / "demo/version-corregida.mjs").read_bytes(), bad.cases, bad.specification, bad.runner)
    monkeypatch.setattr(Snapshot, "capture", lambda: bad)
    agent.tools[0](context)
    assert agent.tools[1](context)["summary"]["failed"] == 2
    monkeypatch.setattr(Snapshot, "capture", lambda: fixed)
    agent.tools[0](context)
    assert agent.tools[1](context)["summary"]["failed"] == 0


def test_practice_starts_with_bug_and_preserves_existing_work(tmp_path):
    from scripts.preparar_practica import prepare

    destination = tmp_path / "equipo"
    prepare(destination)
    assert not (destination / "agente/agent.py").exists()
    assert not (destination / "flujo/agent.py").exists()
    assert (destination / ".agents/skills/verificar/SKILL.md").exists()
    assert execute_tests(Snapshot.capture(destination))["summary"]["failed"] == 2
    with pytest.raises(FileExistsError):
        prepare(destination)


def test_change_during_run_preserves_both_snapshots(monkeypatch, tmp_path):
    import servidor

    first_started = threading.Event()
    release_first = threading.Event()
    original = servidor.run_pipeline

    def delayed(snapshot, mode, trigger, output):
        if not first_started.is_set():
            first_started.set()
            assert release_first.wait(6)
        return original(snapshot, mode, trigger, output)

    monkeypatch.setattr(servidor, "run_pipeline", delayed)
    coordinator = Coordinator(make_workspace(tmp_path))
    coordinator.start()
    try:
        assert first_started.wait(3)
        coordinator.apply_scenario("corregida")
        wait_until(lambda: coordinator.status()["queued"] == 2)
        release_first.set()
        wait_until(lambda: len(read_history(coordinator.output)) == 2)
        reports = read_history(coordinator.output)
        assert {report["summary"]["percentage"] for report in reports} == {50, 100}
        last = json.loads((coordinator.output / "ultimo.json").read_text())
        assert last["summary"]["percentage"] == 100
    finally:
        release_first.set()
        coordinator.stop.set()


def test_presentation_has_no_required_external_assets(tmp_path):
    from html.parser import HTMLParser

    class AssetParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.dependencies = []

        def handle_starttag(self, tag, attributes):
            values = dict(attributes)
            if tag == "script" and values.get("src"):
                self.dependencies.append(values["src"])
            if tag == "link" and "stylesheet" in values.get("rel", "").split():
                self.dependencies.append(values.get("href"))
            if tag in ("img", "iframe") and values.get("src"):
                self.dependencies.append(values["src"])

    copied = tmp_path / "WORKSHOP_GEMINI.html"
    shutil.copy2(ROOT / "WORKSHOP_GEMINI.html", copied)
    parser = AssetParser()
    parser.feed(copied.read_text(encoding="utf-8"))
    assert parser.dependencies == []
