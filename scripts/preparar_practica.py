"""Crea un kit de práctica sin sobrescribir un equipo existente."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for directory in ("app", "contratos", "demo", ".agents", "conocimiento"):
        shutil.copytree(ROOT / directory, destination / directory)
    shutil.copy2(ROOT / "demo/version-con-error.mjs", destination / "app/calculadora.mjs")
    (destination / "scripts").mkdir()
    for name in ("ejecutar-pruebas.mjs",):
        shutil.copy2(ROOT / "scripts" / name, destination / "scripts" / name)
    (destination / "specs").mkdir()
    for name in ("aplicacion.md", "workshop.md"):
        shutil.copy2(ROOT / "specs" / name, destination / "specs" / name)
    for name in ("qa_core.py", "procesar.py", "servidor.py", "iniciar.ps1", "requirements.txt", ".env.example", ".gitignore", "AGENTS.md"):
        shutil.copy2(ROOT / name, destination / name)
    (destination / ".github/workflows").mkdir(parents=True)
    shutil.copy2(ROOT / ".github/workflows/qa.yml", destination / ".github/workflows/qa.yml")
    (destination / "agente").mkdir()
    (destination / "agente/__init__.py").write_text('', encoding="utf-8")
    (destination / "flujo").mkdir()
    (destination / "flujo/__init__.py").write_text('', encoding="utf-8")
    (destination / "pagina").mkdir()
    (destination / "specs/plan.md").write_text(
        "# Plan del equipo\n\nGenera las tareas con /plan a partir de las specs que revise el equipo.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--equipo", default="equipo-01")
    args = parser.parse_args()
    if not args.equipo or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in args.equipo):
        parser.error("Use letras, números, guiones o guiones bajos en el nombre del equipo.")
    path = ROOT / "practica" / args.equipo
    try:
        prepare(path)
    except FileExistsError:
        parser.error("Ese equipo ya existe. Elija otro nombre con --equipo.")
    print(f"Abra esta carpeta en Antigravity: {path}")
    print("El motor, las pruebas y la infraestructura están listos. Construya los agentes y la página con las specs y skills.")
