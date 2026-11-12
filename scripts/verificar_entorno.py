"""Comprueba la práctica sin importar agentes del alumno ni cargar credenciales."""
import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def verify(root: Path = ROOT) -> dict:
    from qa_core import Snapshot, atomic_json, execute_tests

    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("El entorno de la práctica debe usar Python 3.12.")
    for package in ("google.adk", "pytest", "dotenv"):
        importlib.import_module(package)
    node = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout.strip()
    if int(node.lstrip("v").split(".")[0]) < 22:
        raise RuntimeError("Solicita a TI Node 22 o superior.")
    skills = ["especificar", "implementar", "verificar"]
    for skill in skills:
        path = root / ".agents/skills" / skill / "SKILL.md"
        if not path.is_file() or not path.read_text(encoding="utf-8").startswith("---"):
            raise RuntimeError(f"Falta la skill {skill} o su encabezado.")
    result = execute_tests(Snapshot.capture(root))
    summary = result["summary"]
    report = {
        "ready": True,
        "python": sys.version.split()[0],
        "node": node,
        "skills": skills,
        "summary": summary,
        "gemini_called": False,
        "note": "Las fallas de la aplicación son resultados de pruebas, no errores de instalación.",
    }
    atomic_json(root / "salida/preparacion.json", report)
    return report


if __name__ == "__main__":
    try:
        report = verify()
        summary = report["summary"]
        print(f"Entorno listo: Python {report['python']}, Node {report['node']}, ADK y tres skills.")
        print(f"Pruebas locales: {summary['passed']}/{summary['total']} aprobadas ({summary['percentage']} %).")
        print("En el kit nuevo se esperan 2/4 y 50 % por el bug del ejercicio. Si ya lo editaste, se muestran tus resultados actuales.")
        print("Evidencia: salida/preparacion.json. No se llamó a Gemini.")
    except Exception as error:
        print(f"Preparación incompleta: {error}", file=sys.stderr)
        sys.exit(1)
