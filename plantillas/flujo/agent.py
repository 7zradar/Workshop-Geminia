"""Plantilla del flujo QA + revisor. Cópiala a flujo/agent.py y completa los TODO con /implementar.

Lo que ya está resuelto: los modelos de salida (flujo/modelos.py), los imports y la
interfaz que espera procesar.py. Lo que construye el equipo: el agente revisor y la
secuencia que lo conecta con el agente QA del bloque 1.
"""
import os

from google.adk.agents import Agent, SequentialAgent  # noqa: F401  (los usarás al completar los TODO)
from google.adk.models.base_llm import BaseLlm

from agente.agent import create_agent
from flujo.modelos import Analysis, Finding, Review
from qa_core import Evidence

# procesar.py importa Analysis, Review y create_pipeline desde este módulo. No los renombres.
__all__ = ["Analysis", "Finding", "Review", "create_pipeline", "root_agent"]

# TODO 1: escribe la instrucción del revisor a partir de specs/flujo.md.
# ADK reemplaza estas variables con el estado compartido de la sesión:
#   {evidencia}    resultados originales de ejecutar_pruebas (el agente QA los guarda ahí)
#   {diagnostico}  JSON del agente QA (su output_key)
#   {contexto?}    fragmentos recuperados si tu agente usa RAG; el ? lo vuelve opcional
# Debe comprobar: un hallazgo por prueba fallida, esperado y obtenido iguales a la evidencia,
# que ninguna prueba aprobada aparezca como defecto, y responder VALIDADO u OBSERVADO.
REVIEWER_INSTRUCTION = """TODO"""


def create_pipeline(evidence: Evidence | None, model: str | BaseLlm):
    qa = create_agent(evidence, model)  # guarda su diagnóstico en state["diagnostico"]
    # TODO 2: crea el revisor con Agent(...). Requisitos fijos de procesar.py:
    #   name="revisor_qa", instruction=REVIEWER_INSTRUCTION,
    #   output_schema=Review, output_key="revision", include_contents="none"
    #   (sin herramientas: solo evalúa lo que ya está en el estado)
    # TODO 3: devuelve SequentialAgent(name="flujo_qa", sub_agents=[qa, revisor]).
    raise NotImplementedError("Completa el revisor y la secuencia en flujo/agent.py.")


root_agent = create_pipeline(None, os.getenv("GEMINI_MODEL") or "gemini-flash-latest")
