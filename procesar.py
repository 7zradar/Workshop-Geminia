"""Ejecuta QA en modo evidencia o con dos agentes Gemini y persiste un reporte."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from qa_core import ROOT, Evidence, Snapshot, build_report, local_analysis, persist_report, validate_analysis


async def gemini_analysis(evidence: Evidence) -> tuple[dict, dict, list[dict], str]:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("Configure GOOGLE_API_KEY en .env para ejecutar los dos agentes Gemini.")
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    from flujo.agent import Analysis, Review, create_pipeline

    model = os.getenv("GEMINI_MODEL") or "gemini-flash-latest"
    runner = InMemoryRunner(agent=create_pipeline(evidence, model), app_name="workshop_qa")
    session = await runner.session_service.create_session(app_name="workshop_qa", user_id="facilitador")
    trace = []
    try:
        async with asyncio.timeout(150):
            async for event in runner.run_async(
                user_id="facilitador", session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text="Ejecuta QA con ambas herramientas y revisa el diagnóstico.")]),
            ):
                for call in event.get_function_calls():
                    trace.append({"actor": event.author, "event": "tool_call", "name": call.name})
                if event.is_final_response():
                    trace.append({"actor": event.author, "event": "completed", "name": "respuesta"})
        session = await runner.session_service.get_session(
            app_name="workshop_qa", user_id="facilitador", session_id=session.id,
        )
        called = {item["name"] for item in evidence.trace}
        if evidence.result is None or not {"leer_criterios", "ejecutar_pruebas"}.issubset(called):
            raise ValueError("El agente no ejecutó las dos herramientas requeridas.")
        raw = session.state["diagnostico"].strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        analysis = Analysis.model_validate_json(raw).model_dump()
        raw_review = session.state["revision"]
        review = (Review.model_validate_json(raw_review) if isinstance(raw_review, str)
                  else Review.model_validate(raw_review)).model_dump()
        validate_analysis(analysis, evidence.result, evidence.citations)
        return analysis, review, trace, model
    finally:
        await runner.close()


def run_pipeline(snapshot: Snapshot | None = None, mode: str = "evidencia",
                 trigger: str = "manual", output: Path | None = None) -> dict:
    snapshot = snapshot or Snapshot.capture()
    evidence = Evidence(snapshot)
    if mode == "gemini":
        analysis, review, trace, model = asyncio.run(gemini_analysis(evidence))
        result = evidence.result
    elif mode == "evidencia":
        evidence.criteria()
        result = evidence.tests()
        analysis = local_analysis(
            result, lambda query: [item["source"] for item in evidence.context(query)["results"][:2]])
        validate_analysis(analysis, result, evidence.citations)
        review = {"decision": "VALIDADO", "observations": [
            "Comprobación local de correspondencia entre casos fallidos y hallazgos.",
            "El modo evidencia usa pruebas reales y un diagnóstico determinista.",
        ] + (["Las fuentes citadas provienen de la recuperación local sobre conocimiento/."]
             if evidence.citations else [])}
        trace = evidence.trace + [{"actor": "revision_local", "event": "completed", "name": "consistencia"}]
        model = ""
    else:
        raise ValueError("Modo inválido. Elija evidencia o gemini.")
    report = build_report(snapshot, result, analysis, review, trace, mode, trigger, model, evidence.citations)
    persist_report(report, output or ROOT / "salida")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["evidencia", "gemini"], default="evidencia")
    parser.add_argument("--trigger", default="manual")
    parser.add_argument("--output", type=Path, default=ROOT / "salida")
    parser.add_argument("--fail-on-defects", action="store_true")
    args = parser.parse_args()
    try:
        report = run_pipeline(mode=args.mode, trigger=args.trigger, output=args.output)
    except Exception as error:
        if args.mode == "gemini":
            print(f"Error Gemini ({type(error).__name__}). Revise .env, modelo, cuota y conectividad.")
        else:
            print(f"Error de ejecución: {error}")
        return 2
    print(json.dumps({"id": report["id"], "mode": report["mode"], "verdict": report["verdict"],
                      "summary": report["summary"]}, ensure_ascii=False, indent=2))
    return 1 if args.fail_on_defects and report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
