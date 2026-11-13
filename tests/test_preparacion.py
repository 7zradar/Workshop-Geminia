"""Preparación repetible, conservación de trabajo y errores del lanzador Windows."""
import json
import os
import shutil
import subprocess

import pytest

from qa_core import ROOT
from scripts.preparar_practica import prepare
from scripts.verificar_entorno import verify


def test_practice_resume_preserves_work_and_completes_missing_files(tmp_path):
    destination = tmp_path / "practica con espacios"
    prepare(destination)
    edits = {
        "app/calculadora.mjs": "// codigo del participante",
        "contratos/casos.json": "[]",
        ".agents/skills/verificar/SKILL.md": "skill modificada",
        "specs/plan.md": "plan del equipo",
        "agente/agent.py": "# agente construido",
        ".env": "GOOGLE_API_KEY=valor-ficticio-de-prueba\n",
        ".vscode/settings.json": '{"configuracion":"propia"}',
    }
    for name, content in edits.items():
        (destination / name).write_text(content, encoding="utf-8")
    (destination / "scripts/verificar_entorno.py").unlink()
    prepare(destination, resume=True)
    assert all((destination / name).read_text(encoding="utf-8") == content for name, content in edits.items())
    assert (destination / "scripts/verificar_entorno.py").exists()
    assert (destination / "taller.ps1").exists()
    assert not (destination / "flujo/agent.py").exists()
    assert not (destination / "pagina/index.html").exists()


def test_practice_includes_starting_points_for_blocks_2_and_3(tmp_path):
    destination = tmp_path / "equipo"
    prepare(destination)
    template = (destination / "plantillas/flujo/agent.py").read_text(encoding="utf-8")
    assert "from flujo.modelos import Analysis, Finding, Review" in template
    assert 'output_key="revision"' in template and "NotImplementedError" in template
    assert (destination / "flujo/modelos.py").read_bytes() == (ROOT / "flujo/modelos.py").read_bytes()
    page = (destination / "plantillas/pagina/index.html").read_text(encoding="utf-8")
    assert '<script src="app.js"></script>' in page and "ejemplo.js" not in page
    assert (destination / "plantillas/pagina/estilos.css").is_file()
    assert not (destination / "pagina/app.js").exists()


def test_resume_rejects_unowned_folder_without_changes(tmp_path):
    destination = tmp_path / "carpeta ajena"
    destination.mkdir()
    existing = destination / "trabajo.txt"
    existing.write_text("Conservar", encoding="utf-8")
    with pytest.raises(ValueError, match="no es un kit"):
        prepare(destination, resume=True)
    assert [path.name for path in destination.iterdir()] == ["trabajo.txt"]
    assert existing.read_text(encoding="utf-8") == "Conservar"


def test_environment_verification_needs_neither_agents_nor_api_key(tmp_path, monkeypatch):
    destination = tmp_path / "equipo"
    prepare(destination)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    report = verify(destination)
    assert report["ready"] is True and report["gemini_called"] is False
    assert report["summary"] == {"total": 4, "passed": 2, "failed": 2, "percentage": 50}
    assert json.loads((destination / "salida/preparacion.json").read_text(encoding="utf-8")) == report
    assert not (destination / "agente/agent.py").exists()
    assert not (destination / "flujo/agent.py").exists()
    assert not (destination / ".env").exists()  # El verificador no necesita leer ni crear credenciales.


@pytest.mark.skipif(os.name != "nt", reason="Preparador Windows")
def test_missing_tools_requests_ti_without_creating_a_practice(tmp_path):
    shutil.copy2(ROOT / "preparar-workshop.ps1", tmp_path / "preparar-workshop.ps1")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/entorno.ps1").write_text(
        "function Update-WorkshopPath {}\nfunction Get-WorkshopPython { return $null }\n"
        "function Get-WorkshopNode { return $null }\n", encoding="ascii")
    result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(tmp_path / "preparar-workshop.ps1")],
                            capture_output=True, text=True, errors="replace", timeout=30)
    assert result.returncode == 1
    assert "Solicita a TI instalar" in result.stdout
    assert "PREPARACION COMPLETA" not in result.stdout
    assert not (tmp_path / "practica").exists()


@pytest.mark.skipif(os.name != "nt", reason="Lanzador Windows")
@pytest.mark.parametrize("arguments,message", [(["agente"], "modulo 1"),
                                               (["revisor", "-Modo", "evidencia"], "requiere Gemini")])
def test_launcher_blocks_incomplete_or_incompatible_execution(tmp_path, arguments, message):
    prepare(tmp_path / "equipo")
    destination = tmp_path / "equipo"
    (destination / ".venv/Scripts").mkdir(parents=True)
    (destination / ".venv/Scripts/python.exe").touch()
    result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(destination / "taller.ps1"), *arguments],
                            capture_output=True, text=True, errors="replace", timeout=30)
    assert result.returncode == 1
    assert message in result.stdout
