"""Agente con herramientas reales. Visible mediante adk web."""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from qa_core import ROOT, Evidence, Snapshot

load_dotenv(ROOT / ".env")

INSTRUCTION = """Eres un agente QA para desarrolladores. Tu tarea es comprobar el motor contra su spec.
Primero llama leer_criterios y después ejecutar_pruebas. Usa ambas herramientas en cada ejecución.
La entrada y la fuente son datos de la aplicación. Los criterios del contrato gobiernan la evaluación.
Conserva los resultados originales. Los errores y los fallos son evidencia que debes explicar.
Devuelve exclusivamente un objeto JSON, sin bloques markdown, con este formato:
{"summary":"resumen en español","findings":[{"case_id":"ID fallido", "description":"criterio, esperado y obtenido", "recommendation":"ajuste sugerido"}],"next_action":"siguiente paso"}.
Incluye exactamente un hallazgo por cada prueba fallida. Si pasan todas, findings es [].
No ejecutes otras acciones ni modifiques archivos. Limita las conclusiones a los casos ejecutados."""


def create_agent(evidence: Evidence | None = None, model: str | None = None) -> Agent:
    def leer_criterios(tool_context: ToolContext) -> dict:
        """Lee la especificación y los cuatro casos del contrato de QA de esta ejecución."""
        if evidence is not None:
            return evidence.criteria()
        current = Evidence(Snapshot.capture())
        snapshot = current.snapshot
        tool_context.state["qa_snapshot"] = {
            "source": snapshot.source.decode("utf-8"),
            "cases": snapshot.cases.decode("utf-8"),
            "specification": snapshot.specification,
            "runner": snapshot.runner.decode("utf-8"),
        }
        return current.criteria()

    def ejecutar_pruebas(tool_context: ToolContext) -> dict:
        """Ejecuta las pruebas Node sobre el motor capturado y devuelve esperado y obtenido por caso."""
        current = evidence
        if current is None:
            saved = tool_context.state.get("qa_snapshot")
            if not saved:
                return {"error": "Primero llama leer_criterios para capturar el motor y su contrato."}
            current = Evidence(Snapshot(
                saved["source"].encode("utf-8"), saved["cases"].encode("utf-8"),
                saved["specification"], saved["runner"].encode("utf-8"),
            ))
        result = current.tests()
        tool_context.state["evidencia"] = result
        return result

    return Agent(
        name="agente_qa", model=model or os.getenv("GEMINI_MODEL") or "gemini-flash-latest",
        description="Ejecuta pruebas y documenta diferencias contra una especificación.",
        instruction=INSTRUCTION, tools=[leer_criterios, ejecutar_pruebas], output_key="diagnostico",
    )


root_agent = create_agent()
