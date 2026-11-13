"""Modelos de salida que procesar.py valida. El kit los entrega listos."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    description: str
    recommendation: str
    sources: list[str] = Field(default_factory=list)


class Analysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str
    findings: list[Finding]
    next_action: str


class Review(BaseModel):
    # Sin extra="forbid": Gemini rechaza additionalProperties en output_schema.
    decision: Literal["VALIDADO", "OBSERVADO"]
    observations: list[str] = Field(description="Comprobaciones de consistencia o problemas detectados.")
