"""Crea un kit de práctica sin sobrescribir un equipo existente."""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = {"kind": "workshop-qa-practice", "version": 1}


def copy_missing(source: Path, destination: Path) -> None:
    """Completa un kit interrumpido sin reemplazar archivos del participante."""
    if source.is_dir():
        destination.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            copy_missing(child, destination / child.name)
    elif not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def prepare(destination: Path, resume: bool = False) -> None:
    marker = destination / ".workshop-practica.json"
    if destination.exists():
        if not resume:
            raise FileExistsError(destination)
        if not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")) != MARKER:
            raise ValueError("La carpeta existe y no es un kit identificado. No se modificó. Elige otro --equipo.")
    else:
        destination.mkdir(parents=True, exist_ok=False)
        marker.write_text(json.dumps(MARKER), encoding="utf-8")
    for directory in ("app", "contratos", "demo", ".agents", "conocimiento"):
        if directory == "app":
            # La referencia puede estar corregida: el kit nuevo siempre parte con el bug.
            copy_missing(ROOT / "demo/version-con-error.mjs", destination / "app/calculadora.mjs")
        else:
            copy_missing(ROOT / directory, destination / directory)
    for name in ("ejecutar-pruebas.mjs", "probar_revisor.py", "verificar_entorno.py", "entorno.ps1"):
        copy_missing(ROOT / "scripts" / name, destination / "scripts" / name)
    for name in ("aplicacion.md", "workshop.md"):
        copy_missing(ROOT / "specs" / name, destination / "specs" / name)
    for name in ("qa_core.py", "procesar.py", "servidor.py", "iniciar.ps1", "taller.ps1", "requirements.txt", ".env.example", ".gitignore", "AGENTS.md"):
        copy_missing(ROOT / name, destination / name)
    copy_missing(ROOT / ".github/workflows/qa.yml", destination / ".github/workflows/qa.yml")
    for name in ("agente", "flujo", "pagina"):
        (destination / name).mkdir(exist_ok=True)
        if name != "pagina":
            initializer = destination / name / "__init__.py"
            if not initializer.exists():
                initializer.write_text('', encoding="utf-8")
    plan = destination / "specs/plan.md"
    if not plan.exists():
        plan.write_text(
            "# Plan del equipo\n\nGenera las tareas con /plan a partir de las specs que revise el equipo.\n",
            encoding="utf-8",
        )
    settings = destination / ".vscode/settings.json"
    if not settings.exists():
        settings.parent.mkdir(exist_ok=True)
        settings.write_text(json.dumps({"python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--equipo", default="equipo-01")
    parser.add_argument("--reanudar", action="store_true", help="Completa solo archivos ausentes en un kit identificado.")
    args = parser.parse_args()
    if not args.equipo or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in args.equipo):
        parser.error("Use letras, números, guiones o guiones bajos en el nombre del equipo.")
    path = ROOT / "practica" / args.equipo
    try:
        prepare(path, resume=args.reanudar)
    except FileExistsError:
        parser.error("Ese equipo ya existe. Elija otro nombre con --equipo.")
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"Abra esta carpeta en Antigravity: {path}")
    print("El motor, las pruebas y la infraestructura están listos. Construya los agentes y la página con las specs y skills.")
