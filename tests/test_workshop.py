import json
import shutil
import subprocess
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

import pytest

from procesar import run_pipeline
from qa_core import ROOT, Snapshot, execute_tests, read_history, search_knowledge, validate_analysis
from servidor import Coordinator, make_handler


def snapshot_version(name):
    current = Snapshot.capture()
    return Snapshot((ROOT / f"demo/version-{name}.mjs").read_bytes(), current.cases,
                    current.specification, current.runner, current.knowledge)


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
            calls, cited = [], []
            for content in llm_request.contents:
                for part in content.parts or []:
                    if part.function_response:
                        calls.append(part.function_response.name)
                        if part.function_response.name == "buscar_contexto":
                            cited += [item["source"] for item in part.function_response.response["results"][:1]]
            args = {}
            if "leer_criterios" not in calls:
                name = "leer_criterios"
            elif "ejecutar_pruebas" not in calls:
                name = "ejecutar_pruebas"
            elif "buscar_contexto" not in calls:
                name, args = "buscar_contexto", {"consulta": "operaciones gratuitas cobradas"}
            else:
                text = json.dumps({"summary": "Dos pruebas fallidas.", "findings": [
                    {"case_id": identifier, "description": "Esperado y obtenido difieren.",
                     "recommendation": "Corregir el cálculo.", "sources": cited}
                    for identifier in ("QA-02", "QA-03")
                ], "next_action": "Corregir y repetir."})
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))
                return
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name=name, args=args))]))

    original = flow.create_pipeline
    monkeypatch.setattr(flow, "create_pipeline", lambda evidence, model: original(evidence, LocalModel(model="modelo-local-de-prueba")))
    monkeypatch.setenv("GOOGLE_API_KEY", "clave-ficticia-solo-para-el-test")
    report = run_pipeline(snapshot_version("con-error"), mode="gemini", output=tmp_path)
    assert report["summary"]["failed"] == 2
    assert report["review"]["decision"] == "VALIDADO"
    assert {event["actor"] for event in report["trace"]} >= {"agente_qa", "revisor_qa"}
    assert {event["name"] for event in report["trace"]} >= {"leer_criterios", "ejecutar_pruebas", "buscar_contexto"}
    assert all(item["sources"] == ["historial-defectos.md#DEF-101 Cobro de operaciones gratuitas"]
               for item in report["analysis"]["findings"])
    assert report["context"][0]["source"].startswith("historial-defectos.md#DEF-101")


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
    assert (destination / "conocimiento/historial-defectos.md").exists()
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


def test_search_finds_relevant_source_and_ignores_unrelated_queries():  # R1, R2
    snapshot = Snapshot.capture()
    found = search_knowledge(snapshot, "operaciones gratuitas cobradas")
    assert found[0]["source"].startswith("historial-defectos.md#DEF-101")
    assert any(item["source"].startswith("reglas-negocio.md#Tarifa") for item in search_knowledge(
        snapshot, "Las primeras diez operaciones son gratuitas"))
    assert search_knowledge(snapshot, "receta de cocina peruana") == []


def test_evidence_report_cites_retrieved_sources_without_changing_verdict(tmp_path):  # R3, R5, R8
    with_knowledge = snapshot_version("con-error")
    bare = Snapshot(with_knowledge.source, with_knowledge.cases, with_knowledge.specification, with_knowledge.runner)
    report = run_pipeline(with_knowledge, output=tmp_path)
    baseline = run_pipeline(bare, output=tmp_path)
    assert report["summary"] == baseline["summary"] and report["verdict"] == baseline["verdict"] == "CON_FALLAS"
    retrieved = {item["source"] for item in report["context"]}
    findings = report["analysis"]["findings"]
    assert {item["case_id"] for item in findings} == {"QA-02", "QA-03"}
    assert all(item["sources"] and set(item["sources"]) <= retrieved for item in findings)
    assert "buscar_contexto" in {event["name"] for event in report["trace"]}
    assert baseline["context"] == [] and all(item["sources"] == [] for item in baseline["analysis"]["findings"])


def test_report_rejects_invented_sources():  # R4
    result = execute_tests(snapshot_version("con-error"))
    source = "historial-defectos.md#DEF-101 Cobro de operaciones gratuitas"

    def analysis(sources):
        return {"findings": [{"case_id": "QA-02", "sources": sources}, {"case_id": "QA-03", "sources": []}]}

    known = [{"source": source, "title": "t", "excerpt": "e"}]
    validate_analysis(analysis([source]), result, known)
    with pytest.raises(ValueError, match="no se recuperaron"):
        validate_analysis(analysis(["inventado.md#Falso"]), result, known)
    with pytest.raises(ValueError, match="no se recuperaron"):
        validate_analysis(analysis([source]), result)


def test_changing_knowledge_changes_identity_and_no_knowledge_keeps_it():  # R6
    import hashlib

    base = snapshot_version("con-error")
    edited = Snapshot(base.source, base.cases, base.specification, base.runner,
                      base.knowledge + (("nuevo.md", "## DEF-999 Prueba\nTexto."),))
    bare = Snapshot(base.source, base.cases, base.specification, base.runner)
    legacy = hashlib.sha256(f"{bare.source_hash}:{bare.contract_hash}:evidencia:".encode()).hexdigest()[:20]
    assert base.identity("evidencia") != edited.identity("evidencia")
    assert bare.identity("evidencia") == legacy


def test_agent_exposes_context_tool():
    from types import SimpleNamespace
    from agente.agent import create_agent

    agent = create_agent()
    assert [tool.__name__ for tool in agent.tools] == ["leer_criterios", "ejecutar_pruebas", "buscar_contexto"]
    context = SimpleNamespace(state={})
    found = agent.tools[2]("operaciones gratuitas cobradas", context)
    assert found["results"][0]["source"].startswith("historial-defectos.md#DEF-101")
    assert context.state["contexto"][0]["source"] == found["results"][0]["source"]


def test_presentation_has_optional_rag_experience():
    script = (
        "const fs=require('fs'),vm=require('vm');"
        "const h=fs.readFileSync(process.argv[1],'utf8');"
        "const m=h.match(/<script>([\\s\\S]*?window\\.WORKSHOP_MODULES[\\s\\S]*?)<\\/script>/);"
        "const w={};vm.runInNewContext(m[1],{window:w});"
        "console.log(JSON.stringify(w.WORKSHOP_MODULES.map(x=>({id:x.id,optional:!!x.optional,minutes:x.minutes,"
        "steps:x.steps.map(s=>s.minutes),complete:x.steps.every(s=>s.prompt&&s.done&&s.body)}))))"
    )
    out = subprocess.run([shutil.which("node"), "-e", script, str(ROOT / "WORKSHOP_GEMINI.html")],
                         capture_output=True, encoding="utf-8", check=True).stdout
    modules = json.loads(out)
    assert [m["id"] for m in modules] == [1, 2, 3, 4]
    assert all(sum(m["steps"]) == m["minutes"] and m["complete"] for m in modules)
    assert [m["optional"] for m in modules] == [False, False, False, True]
    assert sum(m["minutes"] for m in modules if not m["optional"]) + 35 == 180
    assert [len(m["steps"]) for m in modules] == [6, 6, 5, 5]
