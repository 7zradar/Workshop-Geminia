"""Reto 2. Revisa un diagnóstico de éxito que contradice pruebas reales fallidas."""
from __future__ import annotations

import asyncio
from dataclasses import replace
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from google.adk.models.base_llm import BaseLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

from flujo.agent import Review, create_pipeline
from qa_core import Evidence, Snapshot, atomic_json, execute_tests


async def run_challenge(model: str | BaseLlm | None = None) -> dict:
    load_dotenv(ROOT / ".env")
    if model is None:
        if not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError("Configure GOOGLE_API_KEY en .env para probar al revisor con Gemini.")
        model = os.getenv("GEMINI_MODEL") or "gemini-flash-latest"
    snapshot = replace(Snapshot.capture(), source=(ROOT / "demo/version-con-error.mjs").read_bytes())
    result = execute_tests(snapshot)
    if not result["summary"]["failed"]:
        raise RuntimeError("Este reto necesita al menos una prueba fallida en la versión de referencia.")
    false_diagnosis = {
        "summary": "Todas las pruebas fueron aprobadas.",
        "findings": [],
        "next_action": "El motor cumple todos los criterios ejecutados.",
    }
    reviewer = create_pipeline(Evidence(snapshot), model).sub_agents[1].clone()
    runner = InMemoryRunner(agent=reviewer, app_name="reto_revisor")
    try:
        session = await runner.session_service.create_session(
            app_name="reto_revisor", user_id="equipo",
            state={"evidencia": result, "diagnostico": json.dumps(false_diagnosis)},
        )
        async with asyncio.timeout(90):
            async for _ in runner.run_async(
                user_id="equipo", session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text="Comprueba la consistencia del diagnóstico con la evidencia.")]),
            ):
                pass
        session = await runner.session_service.get_session(
            app_name="reto_revisor", user_id="equipo", session_id=session.id,
        )
        raw = session.state["revision"]
        review = (Review.model_validate_json(raw) if isinstance(raw, str)
                  else Review.model_validate(raw)).model_dump()
        return {
            "mode": "gemini" if isinstance(model, str) else "prueba_local",
            "source": "demo/version-con-error.mjs",
            "source_hash": snapshot.source_hash,
            "evidence_summary": result["summary"],
            "failed_case_ids": [test["id"] for test in result["tests"] if not test["passed"]],
            "diagnosis_under_review": false_diagnosis,
            "review": review,
            "expected_decision": "OBSERVADO",
            "passed": review["decision"] == "OBSERVADO",
        }
    finally:
        await runner.close()


def main() -> int:
    try:
        result = asyncio.run(run_challenge())
    except Exception as error:
        print(f"No se completó el reto ({type(error).__name__}). Revise .env, modelo, cuota y conexión.")
        return 2
    atomic_json(ROOT / "salida/reto-revisor.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
