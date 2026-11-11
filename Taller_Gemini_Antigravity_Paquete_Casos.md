# Taller Gemini y Antigravity · Paquete de casos y textos

> La sesión actual de tres horas se desarrolla en [Taller_QA_Gemini.md](Taller_QA_Gemini.md) y [WORKSHOP_GEMINI.html](WORKSHOP_GEMINI.html). El producto es un agente QA con un revisor y un dashboard. Este paquete conserva los casos bancarios originales como referencia. Sus reglas de cuenta PYME se reutilizan para la aplicación bajo prueba. Las skills activas están en `.agents/skills/`.

TCS Forward Engineering · Ruta Gemini · 3 horas

Este paquete completa todos los bloques vacíos del taller: reglas, workflows, prompts, código de referencia, datos ficticios, preguntas de prueba y solicitudes de `inbox/`. Trae cuatro casos: tres retos de banca y uno libre para el equipo.

| Caso | Usuario | Experiencia 1 · Agente | Experiencia 2 · Flujo | Experiencia 3 · Página |
|---|---|---|---|---|
| **A · Crédito personal** | Cliente que evalúa un préstamo | `consultar_tasa`, `calcular_cuota` | Revisa solicitudes de crédito | Simulador de cuota |
| **B · Reclamos de tarjeta** | Titular que no reconoce un cargo | `consultar_movimientos`, `politica_reclamo` | Revisa reclamos | Pago mínimo vs pago total |
| **C · Cuenta PYME** | Dueño de una pequeña empresa | `requisitos_apertura`, `consultar_comisiones` | Revisa solicitudes de apertura | Costo mensual de la cuenta |
| **D · Caso propio** | Lo define el equipo | 2 herramientas propias | 3 solicitudes propias | 1 cálculo propio |

> **Todos los datos son ficticios.** «Banco Andino» no existe. No se usan clientes, código, sistemas ni nombres reales de ningún banco.

### Cómo se usa

1. En el módulo 00, cada equipo elige un caso y copia su **ficha** en `specs/caso.md`.
2. Los prompts de los módulos 01 a 03 son **iguales para todos los casos**, porque siempre leen `specs/caso.md`. Lo único que cambia por caso está en la sección «Casos»: datos, código de referencia, preguntas de prueba, solicitudes y la descripción de la página.
3. El código de referencia es para **comparar**. El equipo no lo copia: lo escribe el agente de Antigravity a partir de la spec.

### Estructura final del repositorio

```text
taller-gemini/
├── .agents/
│   ├── rules/          sdd.md, pagina.md
│   └── workflows/      especificar.md, implementar.md, verificar.md
├── specs/              caso.md, agente.md, agente-plan.md, flujo.md, flujo-plan.md, pagina.md, pagina-plan.md
├── agente/             __init__.py, agent.py, herramientas.py, data/, .env (copia)
├── flujo/              __init__.py, agent.py, criterios.py
├── tests/              test_herramientas.py
├── inbox/              01_completa.txt, 02_incompleta.txt, 03_fuera_alcance.txt
├── salida/             registro.csv, borradores/   (lo genera procesar.py)
├── pagina/             index.html, estilos.css, app.js, calculo.js, calculo.test.js
├── .github/workflows/  procesar.yml
├── procesar.py
├── pytest.ini
├── .env                (no se sube)
└── .gitignore
```

---

## 00 · Entorno y SDD (15 min) · igual para todos los casos

### Comprobación en la apertura

```bash
python --version && node --version && git --version
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -c "import google.adk; print(google.adk.__version__)"
printf "[pytest]\npythonpath = .\n" > pytest.ini
mkdir -p agente/data flujo tests inbox pagina .github/workflows
```

`pytest.ini` permite que las pruebas importen `agente.herramientas` desde la raíz.

### Elegir el caso

Cree `specs/caso.md` y pegue la **ficha** del caso elegido (sección «Casos»). Haga commit:

```bash
git add specs/caso.md .gitignore pytest.ini && git commit -m "caso elegido"
```

### `.agents/rules/sdd.md` · regla del workspace

```markdown
# Regla SDD del workspace

Trabajamos con Spec-Driven Development. Aplica a toda conversación de este workspace.

1. La especificación en `specs/` es la fuente de verdad. Si el código y la spec no coinciden, gana la spec.
2. No escribas código que no corresponda a una tarea (T1, T2…) de un plan aprobado.
3. Implementa una sola tarea por vez. Al terminar, corre su verificación y detente.
4. Si una petición cambia el alcance, primero propone el cambio en la spec y espera aprobación.
5. Lee `specs/caso.md` antes de especificar o planificar: ahí están el usuario, las herramientas y los datos del caso.
6. Todos los datos son ficticios. No uses nombres, cuentas, tarjetas ni sistemas reales.
7. Las claves solo van en `.env`. Nunca las escribas en el código, en los specs ni en los logs.
8. Python: funciones con type hints y docstring; herramientas que devuelven un dict con `status` "ok" o "error".
9. El modelo se lee de la variable de entorno `GEMINI_MODEL`; nunca lo escribas fijo.
10. Responde y documenta en español.
```

### `.agents/workflows/especificar.md` · `/especificar`

```markdown
---
description: Crea o actualiza una especificación en specs/ antes de escribir código.
---

1. Lee `.agents/rules/sdd.md` y `specs/caso.md`.
2. Si algo importante es ambiguo (usuario, entradas, salidas, límites), haz como máximo 3 preguntas y espera las respuestas.
3. Escribe el archivo que se te indique en `specs/` con estas secciones:
   - Objetivo y usuario
   - Entradas y salidas
   - Diseño (firmas de funciones, esquemas o pantallas, según el caso)
   - Criterios de aceptación: tabla con ID, prueba, resultado esperado y cómo se verifica
   - Fuera de alcance
4. No escribas código. Termina mostrando un resumen de la spec y las decisiones que tomaste.
```

### `.agents/workflows/implementar.md` · `/implementar`

```markdown
---
description: Implementa una sola tarea del plan aprobado y la verifica.
---

1. Lee la tarea indicada (por ejemplo T2) en el archivo de plan de `specs/`. Si no se indica, pregunta cuál.
2. Lee la spec relacionada y respeta `.agents/rules/sdd.md`.
3. Modifica solo los archivos que la tarea menciona. Si necesitas tocar otro, detente y explícalo.
4. Corre el comando de verificación de la tarea en la terminal integrada (por ejemplo `pytest -q`).
5. Muestra el diff, el resultado de la verificación y qué criterio de aceptación cubre. Marca la tarea como hecha en el plan.
6. No avances a la siguiente tarea hasta que el equipo lo pida.
```

### `.agents/workflows/verificar.md` · `/verificar`

```markdown
---
description: Verifica el entregable contra los criterios de aceptación y entrega un walkthrough.
---

1. Lee la spec indicada y su tabla de criterios de aceptación.
2. Corre todas las pruebas automáticas (`pytest -q`, `node --test`, según corresponda).
3. Para cada criterio, ejecuta la comprobación y guarda la evidencia: salida de terminal, traza o captura del navegador.
4. Entrega un walkthrough con una tabla: ID, criterio, evidencia, Cumple (sí/no).
5. Si un criterio no se cumple, no lo corrijas por tu cuenta: explica la causa y propone el cambio en la spec o en el plan.
```

---

## 01 · Agente con ADK (45 min)

### Prompt 1.1 · `/especificar`

```text
/especificar Escribe specs/agente.md para un agente de ADK en Python, a partir de specs/caso.md.

- El agente tiene exactamente las dos herramientas de la ficha. Para cada una, escribe la firma con
  type hints, el docstring que leerá el modelo y la forma del dict de retorno (status "ok" o "error").
- Los datos ficticios van en agente/data/, con el contenido de la ficha.
- Escribe la instrucción del agente: qué hace, qué nunca inventa y qué debe declinar.
- La tabla de criterios lleva columnas ID, pregunta, herramienta esperada y resultado esperado. Va una
  fila por cada pregunta de prueba de la ficha y una más para la pregunta fuera de alcance, que se
  declina sin llamar herramientas.
- Agrega dos criterios técnicos: las herramientas tienen pruebas con pytest que no llaman al modelo, y
  el modelo se lee de GEMINI_MODEL.
- No escribas código todavía.
```

### Prompt 1.2 · Planning

```text
Lee specs/agente.md y genera el Implementation Plan y la Task List. Guárdalos en specs/agente-plan.md.

T1. Datos ficticios en agente/data/ tal como dice la spec.
T2. Herramienta 1 en agente/herramientas.py y sus pruebas en tests/test_herramientas.py.
T3. Herramienta 2 en agente/herramientas.py y sus pruebas.
T4. agente/agent.py con INSTRUCCION, HERRAMIENTAS y root_agent (modelo desde GEMINI_MODEL), y
    agente/__init__.py con "from . import agent".
T5. Guía para probar en adk web con cada pregunta de la tabla de criterios.

En cada tarea indica los archivos que toca, el criterio que cubre y el comando de verificación.
No incluyas nada que no cubra un criterio.
```

### Prompt 1.3 · `/implementar`

```text
/implementar T1 de specs/agente-plan.md. Solo esa tarea; al terminar muestra el diff y la verificación.
```

Repita con T2, T3, T4 y T5.

### Referencias comunes del módulo 01

`agente/__init__.py`

```python
from . import agent
```

`pytest.ini`

```ini
[pytest]
pythonpath = .
```

`herramientas.py`, `agent.py`, las pruebas y los datos de cada caso están en la sección «Casos».

### Verificación

```bash
pytest -q
cp .env agente/.env
adk web          # desde la raíz; elija "agente" en el selector
```

En la pestaña **Events** de `adk web` confirme que cada pregunta llama a la herramienta que indica la spec y que la pregunta fuera de alcance no llama a ninguna. Después escriba `/verificar specs/agente.md`.

---

## 02 · Automatización con un agente revisor (45 min)

### Prompt 2.1 · `/especificar`

```text
/especificar Escribe specs/flujo.md para un proceso sin chat que reutiliza el agente de agente/.

- procesar.py lee cada archivo .txt de inbox/.
- Agente 1, "respondedor": usa las mismas herramientas e instrucción de agente/agent.py, redacta un
  borrador y lo guarda en el estado con output_key "respuesta".
- Agente 2, "revisor": no tiene herramientas. Lee {solicitud} y {respuesta} en su instrucción y
  devuelve, con output_schema, un objeto con:
    estado: "APROBADO" | "OBSERVADO" | "DECLINADO"
    motivos: lista de textos
    faltantes: lista de textos (vacía si no falta nada)
  Usa los criterios de revisión de specs/caso.md.
- Se conectan con un SequentialAgent [respondedor, revisor] en flujo/agent.py.
- Salida: una fila por solicitud en salida/registro.csv (fecha, archivo, estado, motivos, faltantes)
  y el borrador en salida/borradores/<archivo>.md.
- Punto de revisión humana: el flujo prepara y registra; nada se envía al cliente; una persona revisa.
- Disparadores: lunes a viernes a las 8:00 (Lima), push a inbox/ y ejecución manual
  (GitHub Actions, workflow_dispatch). La clave va como secreto GOOGLE_API_KEY.
- Criterios: una fila por cada solicitud de inbox/ con su estado esperado; la revisión siempre cumple
  el esquema; no hay claves en el repositorio.
```

### Prompt 2.2 · Planning

```text
Lee specs/flujo.md y genera el Implementation Plan y la Task List. Guárdalos en specs/flujo-plan.md.

T1. flujo/criterios.py con CRITERIOS_REVISION copiados de specs/caso.md.
T2. flujo/agent.py: modelo Revision (pydantic), respondedor, revisor y root_agent (SequentialAgent).
    flujo/__init__.py con "from . import agent".
T3. procesar.py: crea una sesión por solicitud con state {"solicitud": texto}, ejecuta el flujo y
    escribe registro.csv y los borradores.
T4. Ejecutar python procesar.py con las 3 solicitudes y comparar con los estados esperados.
T5. .github/workflows/procesar.yml con cron, push a inbox/ y workflow_dispatch; sube salida/ como artefacto.

Revisa que output_key "respuesta" y la variable {respuesta} del revisor tengan el mismo nombre.
```

### Referencia · `flujo/agent.py` (igual para todos los casos)

Solo cambia `flujo/criterios.py`, que está en cada caso.

```python
import os
from typing import Literal

from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from pydantic import BaseModel, Field

from agente.agent import HERRAMIENTAS, INSTRUCCION
from .criterios import CRITERIOS_REVISION

load_dotenv()
MODELO = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


class Revision(BaseModel):
    estado: Literal["APROBADO", "OBSERVADO", "DECLINADO"] = Field(
        description="APROBADO si la solicitud está completa y la respuesta es correcta; "
        "OBSERVADO si faltan datos o la respuesta tiene errores; "
        "DECLINADO si la solicitud está fuera de alcance."
    )
    motivos: list[str] = Field(description="Motivos breves de la decisión.")
    faltantes: list[str] = Field(description="Datos que faltan en la solicitud; vacío si no falta nada.")


respondedor = Agent(
    name="respondedor",
    model=MODELO,
    instruction=INSTRUCCION
    + "\nResponde la siguiente solicitud como un borrador para que una persona lo revise:\n{solicitud}",
    tools=HERRAMIENTAS,
    output_key="respuesta",
)

revisor = Agent(
    name="revisor",
    model=MODELO,
    instruction=f"""Eres el revisor de calidad. No respondes al cliente: evalúas.
Solicitud original:
{{solicitud}}

Borrador de respuesta:
{{respuesta}}

Criterios:
{CRITERIOS_REVISION}

Devuelve solo el objeto con estado, motivos y faltantes.""",
    output_schema=Revision,
    output_key="revision",
    include_contents="none",
)

root_agent = SequentialAgent(name="flujo", sub_agents=[respondedor, revisor])
```

`include_contents="none"` hace que el revisor evalúe solo lo que recibe en su instrucción (la solicitud y el borrador) y no la conversación completa.

### Referencia · `procesar.py`

```python
"""Procesa cada solicitud de inbox/ con el flujo de dos agentes y registra el resultado.

El flujo solo prepara y registra: una persona revisa salida/registro.csv y los
borradores antes de enviar cualquier respuesta.
"""
import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()
from flujo.agent import root_agent  # noqa: E402  (después de cargar .env)

INBOX = Path("inbox")
SALIDA = Path("salida")
BORRADORES = SALIDA / "borradores"
REGISTRO = SALIDA / "registro.csv"
APP = "flujo"


async def procesar(runner: InMemoryRunner, archivo: Path) -> dict:
    texto = archivo.read_text(encoding="utf-8").strip()
    sesion = await runner.session_service.create_session(
        app_name=APP, user_id="procesador", state={"solicitud": texto}
    )
    mensaje = types.Content(role="user", parts=[types.Part(text=texto)])
    async for _ in runner.run_async(
        user_id="procesador", session_id=sesion.id, new_message=mensaje
    ):
        pass
    sesion = await runner.session_service.get_session(
        app_name=APP, user_id="procesador", session_id=sesion.id
    )
    revision = sesion.state.get("revision") or {}
    if isinstance(revision, str):
        revision = json.loads(revision)
    respuesta = sesion.state.get("respuesta", "")
    (BORRADORES / f"{archivo.stem}.md").write_text(respuesta, encoding="utf-8")
    return {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "archivo": archivo.name,
        "estado": revision.get("estado", "ERROR"),
        "motivos": " | ".join(revision.get("motivos", [])),
        "faltantes": " | ".join(revision.get("faltantes", [])),
    }


async def main() -> None:
    BORRADORES.mkdir(parents=True, exist_ok=True)
    runner = InMemoryRunner(agent=root_agent, app_name=APP)
    filas = [await procesar(runner, a) for a in sorted(INBOX.glob("*.txt"))]
    nuevo = not REGISTRO.exists()
    with open(REGISTRO, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["fecha", "archivo", "estado", "motivos", "faltantes"])
        if nuevo:
            w.writeheader()
        w.writerows(filas)
    for fila in filas:
        print(f"{fila['archivo']}: {fila['estado']}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Referencia · `.github/workflows/procesar.yml`

```yaml
name: procesar-solicitudes

on:
  schedule:
    - cron: "0 13 * * 1-5"   # 8:00 a. m. en Lima (UTC-5), lunes a viernes
  push:
    paths:
      - "inbox/**"
  workflow_dispatch:

jobs:
  procesar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install google-adk pydantic python-dotenv
      - run: python procesar.py
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          GOOGLE_GENAI_USE_VERTEXAI: "FALSE"
          GEMINI_MODEL: ${{ vars.GEMINI_MODEL }}
      - uses: actions/upload-artifact@v4
        with:
          name: registro
          path: salida/
```

En GitHub, en **Settings → Secrets and variables → Actions**:
- Secret `GOOGLE_API_KEY`: la clave de AI Studio.
- Variable `GEMINI_MODEL`: el nombre del modelo Flash vigente.

### Verificación

```bash
python procesar.py
cat salida/registro.csv
```

Debe quedar una fila por solicitud con el estado esperado del caso. Luego ejecute el workflow desde **Actions → procesar-solicitudes → Run workflow** y descargue el artefacto `registro`.

---

## 03 · Vibe coding: página (55 min)

### 3.1 · `.agents/rules/pagina.md`

```markdown
# Principios de la página

Aplica a toda tarea dentro de pagina/.

1. HTML, CSS y JavaScript sin frameworks ni dependencias externas. Debe abrir con doble clic o con
   un servidor estático simple.
2. El cálculo vive en pagina/calculo.js como funciones puras exportadas, sin tocar el DOM, con
   pruebas en pagina/calculo.test.js que se corren con `node --test pagina/`.
3. Responsive desde 360 px de ancho. Todo se puede usar con teclado y el foco es visible.
4. Cada campo tiene <label>. Los errores se muestran junto al campo, en texto, no solo con color.
5. Los montos se muestran en soles con 2 decimales (S/ 1,234.56) y las tasas en porcentaje.
6. Siempre está visible el aviso: "Simulación con datos ficticios. Banco Andino no existe."
7. Sin claves, sin llamadas a APIs y sin datos personales. Los datos ficticios van en un objeto
   dentro de calculo.js.
8. Contraste de texto AA como mínimo.
```

### 3.2 · `/especificar`

Hay un texto por caso; está en la sección «Casos».

### 3.3 · Planning

```text
Lee specs/pagina.md y .agents/rules/pagina.md y genera el Implementation Plan y la Task List.
Guárdalos en specs/pagina-plan.md.

- El stack es el de la regla: HTML, CSS y JS sin dependencias.
- Primero calculo.js y calculo.test.js con el caso calculado a mano de la spec; después la interfaz.
- Cada tarea indica qué criterio de specs/pagina.md cubre y cómo se verifica.
- No agregues funciones, pantallas ni estilos que no pida un criterio.
- La última tarea deja la página lista para GitHub Pages (pagina/index.html como entrada).
```

### 3.4 · `/verificar`

```text
/verificar specs/pagina.md

1. Corre node --test pagina/ y muestra el resultado.
2. Abre pagina/index.html en tu navegador.
3. Prueba cada criterio de la tabla: ingresa el caso calculado a mano y compara con lo esperado,
   prueba un valor inválido y recorre la página solo con Tab y Enter.
4. Toma una captura por criterio y otra con el ancho de un celular (375 px).
5. Entrega el walkthrough con ID, criterio, evidencia y Cumple. Si algo falla, propone el cambio en la spec.
```

### Publicar con GitHub Pages

En **Settings → Pages**, elija la rama `main` y la carpeta `/ (root)`. El enlace queda en `https://<usuario>.github.io/<repo>/pagina/`.

---

# Casos

---

## Caso A · Crédito personal

### Ficha · copiar en `specs/caso.md`

```markdown
# Caso A · Crédito personal (Banco Andino, ficticio)

Usuario: persona que evalúa un préstamo personal y quiere saber su tasa y su cuota antes de pedirlo.
Problema: no sabe cuánto pagará al mes ni cuánto pagará en intereses.

## Herramientas del agente
- consultar_tasa(producto: str, plazo_meses: int) -> dict
  Busca la TEA en agente/data/tasas.csv. Productos: "personal", "consolidacion".
- calcular_cuota(monto: float, tea: float, plazo_meses: int) -> dict
  Sistema francés: TEM = (1 + TEA)^(1/12) - 1; cuota = monto x TEM / (1 - (1 + TEM)^-n).
  Devuelve tem, cuota, total_pagado y total_intereses (2 decimales).

## Datos ficticios · agente/data/tasas.csv
producto,plazo_min,plazo_max,tea
personal,6,11,0.24
personal,12,24,0.18
personal,25,60,0.16
consolidacion,12,36,0.15
consolidacion,37,60,0.14

## Preguntas de prueba
1. ¿Qué tasa tiene un préstamo personal a 12 meses? → consultar_tasa → TEA 18 %
2. Con una TEA de 15 %, ¿cuánto pago al mes por S/ 5 000 a 24 meses? → calcular_cuota → S/ 240.20
3. Quiero S/ 10 000 en préstamo personal a 12 meses, ¿cuál sería mi cuota? → consultar_tasa y calcular_cuota → S/ 910.46
4. ¿Qué tasa tiene un préstamo vehicular a 36 meses? → consultar_tasa (error) → explica que no existe ese producto
Fuera de alcance: «¿Me van a aprobar el préstamo?» → declina sin herramientas

## Criterios de revisión del flujo
- APROBADO: tiene monto, plazo e ingreso mensual, y el borrador usa tasa y cuota de las herramientas.
- OBSERVADO: falta alguno de esos datos o el borrador da números sin calcularlos.
- DECLINADO: pide aprobar o rechazar un crédito, asesoría de inversión u otro tema.

## Página
Simulador de cuota con cronograma. Caso a mano: S/ 10 000, 12 meses, TEA 18 % → cuota S/ 910.46.
```

### Referencia · `agente/data/tasas.csv`

```csv
producto,plazo_min,plazo_max,tea
personal,6,11,0.24
personal,12,24,0.18
personal,25,60,0.16
consolidacion,12,36,0.15
consolidacion,37,60,0.14
```

### Referencia · `agente/herramientas.py`

```python
"""Herramientas del agente de crédito personal (Banco Andino, datos ficticios)."""
import csv
from pathlib import Path

DATOS = Path(__file__).parent / "data" / "tasas.csv"


def consultar_tasa(producto: str, plazo_meses: int) -> dict:
    """Devuelve la TEA ficticia de un producto de crédito para un plazo.

    Úsala cuando el cliente pregunte qué tasa le corresponde a un producto
    (por ejemplo "personal" o "consolidacion") y a un plazo en meses.

    Args:
        producto: nombre del producto: "personal" o "consolidacion".
        plazo_meses: plazo del crédito en meses.

    Returns:
        {"status": "ok", "producto", "plazo_meses", "tea"} con la TEA como
        decimal (0.18 = 18 %), o {"status": "error", "mensaje"} si no existe.
    """
    producto = producto.strip().lower()
    with open(DATOS, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if (
                fila["producto"] == producto
                and int(fila["plazo_min"]) <= plazo_meses <= int(fila["plazo_max"])
            ):
                return {
                    "status": "ok",
                    "producto": producto,
                    "plazo_meses": plazo_meses,
                    "tea": float(fila["tea"]),
                }
    return {
        "status": "error",
        "mensaje": f"No hay tasa para '{producto}' a {plazo_meses} meses.",
    }


def calcular_cuota(monto: float, tea: float, plazo_meses: int) -> dict:
    """Calcula la cuota mensual fija de un crédito con el sistema francés.

    Úsala cuando el cliente quiera saber cuánto pagará al mes. Si no conoce
    la TEA, primero usa consultar_tasa.

    Args:
        monto: monto del préstamo en soles (mayor que 0).
        tea: tasa efectiva anual como decimal (0.18 = 18 %).
        plazo_meses: número de cuotas mensuales (mayor que 0).

    Returns:
        {"status": "ok", "tem", "cuota", "total_pagado", "total_intereses"}
        con montos redondeados a 2 decimales, o {"status": "error", "mensaje"}.
    """
    if monto <= 0 or plazo_meses <= 0 or tea < 0:
        return {"status": "error", "mensaje": "Monto, plazo y TEA deben ser positivos."}
    tem = (1 + tea) ** (1 / 12) - 1
    if tem == 0:
        cuota = monto / plazo_meses
    else:
        cuota = monto * tem / (1 - (1 + tem) ** -plazo_meses)
    total = cuota * plazo_meses
    return {
        "status": "ok",
        "tem": round(tem, 6),
        "cuota": round(cuota, 2),
        "total_pagado": round(total, 2),
        "total_intereses": round(total - monto, 2),
    }
```

### Referencia · `agente/agent.py`

```python
import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .herramientas import calcular_cuota, consultar_tasa

load_dotenv()

INSTRUCCION = """Eres el asistente de créditos personales de Banco Andino (banco ficticio).
- Para tasas usa consultar_tasa; para cuotas usa calcular_cuota. Nunca inventes números.
- Si te falta el monto, el plazo o el producto, pídelo antes de calcular.
- Presenta montos en soles con 2 decimales y la TEA en porcentaje.
- No apruebas ni rechazas créditos, no das asesoría de inversión ni pides datos personales.
  Si te lo piden, declina con amabilidad y explica qué sí puedes hacer.
- Recuerda al final que los datos son ficticios."""

HERRAMIENTAS = [consultar_tasa, calcular_cuota]

root_agent = Agent(
    name="agente_credito",
    model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
    description="Responde dudas de tasas y cuotas de créditos personales ficticios.",
    instruction=INSTRUCCION,
    tools=HERRAMIENTAS,
)
```

### Referencia · `tests/test_herramientas.py`

```python
from agente.herramientas import calcular_cuota, consultar_tasa


def test_tasa_personal_12_meses():
    r = consultar_tasa("personal", 12)
    assert r["status"] == "ok" and r["tea"] == 0.18


def test_tasa_inexistente():
    assert consultar_tasa("vehicular", 12)["status"] == "error"


def test_cuota_caso_a_mano():
    # S/ 10 000, TEA 18 %, 12 meses -> TEM 1.3888 %, cuota S/ 910.46
    r = calcular_cuota(10000, 0.18, 12)
    assert r["cuota"] == 910.46
    assert r["total_intereses"] == 925.57


def test_cuota_monto_invalido():
    assert calcular_cuota(0, 0.18, 12)["status"] == "error"
```

### Referencia · `flujo/criterios.py`

```python
CRITERIOS_REVISION = """- APROBADO: la solicitud indica monto, plazo en meses e ingreso mensual, y el borrador
  usa una tasa y una cuota que provienen de las herramientas.
- OBSERVADO: falta alguno de esos tres datos, o el borrador da números sin calcularlos.
  Lista en faltantes los datos que no están.
- DECLINADO: la solicitud pide aprobar o rechazar un crédito, asesoría de inversión
  o algo que no sea simular un crédito personal."""
```

### Preguntas de prueba en `adk web`

```text
1. ¿Qué tasa tiene un préstamo personal a 12 meses?
2. Con una TEA de 15 %, ¿cuánto pago al mes por S/ 5 000 a 24 meses?
3. Quiero S/ 10 000 en préstamo personal a 12 meses, ¿cuál sería mi cuota?
4. ¿Qué tasa tiene un préstamo vehicular a 36 meses?
Fuera de alcance: ¿Me van a aprobar el préstamo?
```

| # | Herramienta esperada | Resultado esperado |
|---|---|---|
| 1 | `consultar_tasa` | TEA 18 % |
| 2 | `calcular_cuota` | Cuota S/ 240.20; intereses S/ 764.83 |
| 3 | `consultar_tasa` → `calcular_cuota` | TEA 18 %; cuota S/ 910.46; intereses S/ 925.57 |
| 4 | `consultar_tasa` (error) | Explica que no hay producto vehicular y ofrece los que existen |
| Fuera | ninguna | Declina: no aprueba créditos |

### Solicitudes de `inbox/`

`inbox/01_completa.txt` → **APROBADO**
```text
Hola, quiero un préstamo personal de S/ 10 000 a 12 meses. Gano S/ 4 500 al mes. ¿Cuánto pagaría de cuota?
```

`inbox/02_incompleta.txt` → **OBSERVADO** (faltan monto e ingreso mensual)
```text
Quiero un préstamo personal a 18 meses. ¿Cuánto pagaría?
```

`inbox/03_fuera_alcance.txt` → **DECLINADO**
```text
Tengo S/ 20 000 ahorrados. ¿En qué acciones me conviene invertir este año?
```

### 3.2 · `/especificar` de la página

```text
/especificar Escribe specs/pagina.md para un simulador de crédito personal de Banco Andino (ficticio).

Para quién: una persona que quiere saber, antes de pedir un préstamo, cuánto pagará al mes y en total.
Qué hace:
- Pide monto (S/ 500 a S/ 50 000), plazo (6 a 60 meses) y producto (personal o consolidación).
- Toma la TEA de la tabla de specs/caso.md según producto y plazo, y la muestra.
- Muestra la cuota mensual, el total pagado, el total de intereses y el cronograma
  (mes, cuota, interés, amortización, saldo).
- Si el plazo no tiene tasa para ese producto, lo explica junto al campo.
- Muestra el aviso de datos ficticios.
Caso calculado a mano (criterio obligatorio): S/ 10 000, personal, 12 meses → TEA 18 %, TEM 1.3888 %,
cuota S/ 910.46, intereses S/ 925.57. Mes 1: interés S/ 138.88, amortización S/ 771.58, saldo S/ 9,228.42.
Sin tecnología en esta spec; eso lo decide el plan.
```

---

## Caso B · Reclamos de tarjeta de crédito

### Ficha · copiar en `specs/caso.md`

```markdown
# Caso B · Reclamos de tarjeta (Banco Andino, ficticio)

Usuario: titular de una tarjeta de crédito que ve un cargo que no reconoce o que está duplicado.
Problema: no sabe si el cargo existe, qué tipo de reclamo le corresponde ni qué plazo tiene.

## Herramientas del agente
- consultar_movimientos(id_tarjeta: str) -> dict
  Lee agente/data/movimientos.csv. El identificador es ficticio (TJ-1001); nunca se pide el número de tarjeta.
- politica_reclamo(tipo: str) -> dict
  Lee agente/data/politicas.json. Tipos: consumo_no_reconocido, cargo_duplicado, cobro_no_procesado.

## Datos ficticios
movimientos.csv y politicas.json (ver referencias del caso B).

## Preguntas de prueba
1. Revisa los movimientos de mi tarjeta TJ-1001 → consultar_movimientos → 4 movimientos
2. ¿Qué plazo tengo para reclamar un cargo duplicado? → politica_reclamo → 60 días
3. En mi tarjeta TJ-1001 me cobraron dos veces StreamPlus, ¿qué hago? → ambas → cargo duplicado de S/ 39.90 del 2026-11-03 y pasos
4. ¿Cómo reclamo un robo de tarjeta? → politica_reclamo (error) → explica los tipos que existen
Fuera de alcance: «Bloquea la tarjeta de mi esposo, es la TJ-1002» → declina sin herramientas

## Criterios de revisión del flujo
- APROBADO: tiene fecha, monto y comercio, y el borrador usa la política correcta.
- OBSERVADO: falta fecha, monto o comercio, o el borrador inventa plazos o repite claves o números de tarjeta.
- DECLINADO: pide claves, números de tarjeta, actuar sobre la tarjeta de otra persona u otro tema.

## Página
Comparador «pago mínimo vs pago total». Caso a mano: deuda S/ 2 000, TEA 60 %, 6 meses,
pago mínimo = 5 % del saldo con intereses (mínimo S/ 50) → intereses S/ 465.12 y saldo final S/ 1,859.66.
```

### Referencia · `agente/data/movimientos.csv`

```csv
id_tarjeta,fecha,comercio,monto,estado
TJ-1001,2026-11-02,Supermercado La Canasta,184.50,procesado
TJ-1001,2026-11-03,StreamPlus Suscripción,39.90,procesado
TJ-1001,2026-11-03,StreamPlus Suscripción,39.90,procesado
TJ-1001,2026-11-05,TiendaOnline Global,620.00,procesado
TJ-1002,2026-11-01,Grifo El Sol,150.00,procesado
TJ-1002,2026-11-04,Restaurante Mar Azul,98.00,pendiente
```

### Referencia · `agente/data/politicas.json`

```json
{
  "consumo_no_reconocido": {
    "plazo_dias": 30,
    "requisitos": ["fecha del consumo", "monto", "comercio", "declaración de no reconocimiento"],
    "pasos": ["Bloquear la tarjeta desde la app", "Registrar el reclamo", "Recibir respuesta en 15 días hábiles"]
  },
  "cargo_duplicado": {
    "plazo_dias": 60,
    "requisitos": ["fecha del consumo", "monto", "comercio"],
    "pasos": ["Registrar el reclamo", "Recibir respuesta en 10 días hábiles"]
  },
  "cobro_no_procesado": {
    "plazo_dias": 60,
    "requisitos": ["fecha del consumo", "monto", "comercio", "comprobante de anulación"],
    "pasos": ["Adjuntar el comprobante", "Registrar el reclamo", "Recibir respuesta en 15 días hábiles"]
  }
}
```

### Referencia · `agente/herramientas.py`

```python
"""Herramientas del agente de reclamos de tarjeta (Banco Andino, datos ficticios)."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def consultar_movimientos(id_tarjeta: str) -> dict:
    """Lista los movimientos ficticios de una tarjeta a partir de su identificador.

    Úsala cuando el cliente quiera revisar o identificar un consumo. El
    identificador tiene la forma "TJ-1001"; nunca pidas el número de tarjeta.

    Args:
        id_tarjeta: identificador interno ficticio, por ejemplo "TJ-1001".

    Returns:
        {"status": "ok", "id_tarjeta", "movimientos": [{"fecha", "comercio",
        "monto", "estado"}]} o {"status": "error", "mensaje"}.
    """
    id_tarjeta = id_tarjeta.strip().upper()
    with open(DATA / "movimientos.csv", encoding="utf-8") as f:
        movs = [
            {"fecha": r["fecha"], "comercio": r["comercio"], "monto": float(r["monto"]), "estado": r["estado"]}
            for r in csv.DictReader(f)
            if r["id_tarjeta"] == id_tarjeta
        ]
    if not movs:
        return {"status": "error", "mensaje": f"No hay movimientos para {id_tarjeta}."}
    return {"status": "ok", "id_tarjeta": id_tarjeta, "movimientos": movs}


def politica_reclamo(tipo: str) -> dict:
    """Devuelve el plazo, los requisitos y los pasos para un tipo de reclamo.

    Úsala cuando el cliente pregunte cómo reclamar o qué necesita.

    Args:
        tipo: "consumo_no_reconocido", "cargo_duplicado" o "cobro_no_procesado".

    Returns:
        {"status": "ok", "tipo", "plazo_dias", "requisitos", "pasos"} o
        {"status": "error", "mensaje", "tipos_validos"}.
    """
    politicas = json.loads((DATA / "politicas.json").read_text(encoding="utf-8"))
    tipo = tipo.strip().lower()
    if tipo not in politicas:
        return {"status": "error", "mensaje": f"Tipo '{tipo}' no existe.", "tipos_validos": list(politicas)}
    return {"status": "ok", "tipo": tipo, **politicas[tipo]}
```

### Referencia · `agente/agent.py`

```python
import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .herramientas import consultar_movimientos, politica_reclamo

load_dotenv()

INSTRUCCION = """Eres el asistente de reclamos de tarjeta de Banco Andino (banco ficticio).
- Para revisar consumos usa consultar_movimientos con el identificador TJ-xxxx.
- Para explicar cómo reclamar usa politica_reclamo. Nunca inventes plazos ni requisitos.
- Nunca pidas ni repitas números de tarjeta, claves, CVV ni códigos de verificación.
- Solo atiendes al titular: no bloqueas ni consultas tarjetas de terceros.
- Si la consulta no es sobre consumos o reclamos de tarjeta, declina con amabilidad.
- Recuerda al final que los datos son ficticios."""

HERRAMIENTAS = [consultar_movimientos, politica_reclamo]

root_agent = Agent(
    name="agente_reclamos",
    model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
    description="Ayuda a revisar consumos y a iniciar reclamos de tarjeta ficticios.",
    instruction=INSTRUCCION,
    tools=HERRAMIENTAS,
)
```

### Referencia · `tests/test_herramientas.py`

```python
from agente.herramientas import consultar_movimientos, politica_reclamo


def test_movimientos_tarjeta_existente():
    r = consultar_movimientos("tj-1001")
    assert r["status"] == "ok" and len(r["movimientos"]) == 4


def test_detecta_cargo_duplicado_en_datos():
    movs = consultar_movimientos("TJ-1001")["movimientos"]
    streamplus = [m for m in movs if m["comercio"] == "StreamPlus Suscripción"]
    assert len(streamplus) == 2


def test_tarjeta_inexistente():
    assert consultar_movimientos("TJ-9999")["status"] == "error"


def test_politica_cargo_duplicado():
    r = politica_reclamo("cargo_duplicado")
    assert r["status"] == "ok" and r["plazo_dias"] == 60


def test_politica_invalida():
    r = politica_reclamo("robo")
    assert r["status"] == "error" and "consumo_no_reconocido" in r["tipos_validos"]
```

### Referencia · `flujo/criterios.py`

```python
CRITERIOS_REVISION = """- APROBADO: la solicitud indica fecha, monto y comercio del consumo, y el borrador
  usa la política que devuelve politica_reclamo (plazo y requisitos correctos).
- OBSERVADO: falta la fecha, el monto o el comercio, o el borrador inventa plazos.
  Lista en faltantes los datos que no están.
- DECLINADO: la solicitud pide claves, números de tarjeta, actuar sobre la tarjeta
  de otra persona o algo que no sea un consumo o reclamo de tarjeta.
- Si el borrador repite un número de tarjeta o una clave, marca OBSERVADO."""
```

### Preguntas de prueba en `adk web`

```text
1. Revisa los movimientos de mi tarjeta TJ-1001.
2. ¿Qué plazo tengo para reclamar un cargo duplicado?
3. En mi tarjeta TJ-1001 me cobraron dos veces StreamPlus, ¿qué hago?
4. ¿Cómo reclamo un robo de tarjeta?
Fuera de alcance: Bloquea la tarjeta de mi esposo, es la TJ-1002.
```

| # | Herramienta esperada | Resultado esperado |
|---|---|---|
| 1 | `consultar_movimientos` | 4 movimientos; StreamPlus aparece dos veces |
| 2 | `politica_reclamo` | 60 días; requisitos: fecha, monto, comercio |
| 3 | `consultar_movimientos` → `politica_reclamo` | Identifica el cargo duplicado de S/ 39.90 del 2026-11-03 y da los pasos |
| 4 | `politica_reclamo` (error) | Explica los 3 tipos de reclamo que existen |
| Fuera | ninguna | Declina: solo atiende al titular |

### Solicitudes de `inbox/`

`inbox/01_completa.txt` → **APROBADO**
```text
Soy titular de la tarjeta TJ-1001. El 2026-11-03 me cobraron dos veces S/ 39.90 en StreamPlus Suscripción. Quiero reclamar el cargo duplicado.
```

`inbox/02_incompleta.txt` → **OBSERVADO** (faltan fecha, monto y comercio)
```text
Me apareció un cobro raro en mi tarjeta TJ-1001 y quiero reclamar.
```

`inbox/03_fuera_alcance.txt` → **DECLINADO**
```text
Olvidé la clave de mi tarjeta. ¿Me la pueden enviar por aquí?
```

### 3.2 · `/especificar` de la página

```text
/especificar Escribe specs/pagina.md para un comparador «pago mínimo vs pago total» de tarjeta de
crédito de Banco Andino (ficticio).

Para quién: titular que no sabe cuánto le cuesta pagar solo el mínimo.
Qué hace:
- Pide la deuda actual (S/ 100 a S/ 30 000), la TEA (por defecto 60 %) y el número de meses (1 a 24).
- Supone que no hay compras nuevas. Cada mes: interés = saldo x TEM; saldo += interés;
  pago mínimo = 5 % del saldo con intereses, mínimo S/ 50; saldo -= pago.
- Muestra dos columnas: «pago total» (paga toda la deuda el mes 1: S/ 0 de intereses) y «pago mínimo»
  (total pagado, total de intereses y saldo que queda), más una tabla mes a mes.
- Destaca en una frase cuánto queda debiendo pagando solo el mínimo.
- Muestra el aviso de datos ficticios.
Caso calculado a mano (criterio obligatorio): deuda S/ 2 000, TEA 60 %, 6 meses → TEM 3.9944 %;
mes 1: interés S/ 79.89, pago S/ 103.99, saldo S/ 1,975.90; total pagado S/ 605.46,
intereses S/ 465.12, saldo final S/ 1,859.66.
Sin tecnología en esta spec; eso lo decide el plan.
```

---

## Caso C · Apertura de cuenta para PYME

### Ficha · copiar en `specs/caso.md`

```markdown
# Caso C · Cuenta PYME (Banco Andino, ficticio)

Usuario: dueño de una pequeña empresa que quiere abrir una cuenta para su negocio.
Problema: no sabe qué documentos necesita según su tipo de empresa ni cuánto le costará la cuenta al mes.

## Herramientas del agente
- requisitos_apertura(tipo_empresa: str) -> dict
  Lee agente/data/requisitos.json. Tipos: persona_natural_negocio, eirl, sac.
- consultar_comisiones(tipo_cuenta: str) -> dict
  Lee agente/data/comisiones.csv. Cuentas: cuenta_corriente_pyme, cuenta_negocios.
  Costo mensual = mantenimiento + max(0, operaciones - libres) x operación adicional
                  + interbancarias x comisión interbancaria.

## Datos ficticios
requisitos.json y comisiones.csv (ver referencias del caso C).

## Preguntas de prueba
1. ¿Qué documentos necesito para abrir una cuenta si mi empresa es EIRL? → requisitos_apertura → 4 documentos, incluida la vigencia de poder
2. ¿Cuánto cuesta mantener la cuenta corriente PYME? → consultar_comisiones → S/ 25.00 al mes y 10 operaciones libres
3. Somos una SAC: ¿qué necesitamos y cuánto nos costaría la cuenta corriente PYME con 20 operaciones y 4 interbancarias al mes? → ambas → documentos de SAC y S/ 74.00
4. ¿Y la cuenta de negocios con el mismo uso? → consultar_comisiones → S/ 94.50
Fuera de alcance: «¿Cómo hago para pagar menos impuesto a la renta?» → declina sin herramientas

## Criterios de revisión del flujo
- APROBADO: indica el tipo de empresa y menciona todos los documentos que exige ese tipo.
- OBSERVADO: falta el tipo de empresa o algún documento (por ejemplo, la vigencia de poder).
- DECLINADO: pide asesoría tributaria, legal o contable, u otro tema.

## Página
Calculadora del costo mensual que compara las dos cuentas.
Caso a mano: 20 operaciones y 4 interbancarias → cuenta corriente PYME S/ 74.00; cuenta de negocios S/ 94.50.
```

### Referencia · `agente/data/requisitos.json`

```json
{
  "persona_natural_negocio": {
    "documentos": ["DNI del titular", "RUC activo", "recibo de servicio del local"],
    "observacion": "La cuenta se abre a nombre del titular con su RUC."
  },
  "eirl": {
    "documentos": ["RUC activo", "escritura de constitución", "vigencia de poder del titular gerente", "DNI del titular gerente"],
    "observacion": "La vigencia de poder no debe tener más de 30 días."
  },
  "sac": {
    "documentos": ["RUC activo", "escritura de constitución", "vigencia de poder de los representantes", "DNI de los representantes"],
    "observacion": "Si hay firmas conjuntas, deben presentarse todos los representantes."
  }
}
```

### Referencia · `agente/data/comisiones.csv`

```csv
tipo_cuenta,concepto,monto
cuenta_corriente_pyme,mantenimiento_mensual,25.00
cuenta_corriente_pyme,operaciones_libres,10
cuenta_corriente_pyme,operacion_adicional,2.50
cuenta_corriente_pyme,transferencia_interbancaria,6.00
cuenta_negocios,mantenimiento_mensual,12.00
cuenta_negocios,operaciones_libres,5
cuenta_negocios,operacion_adicional,3.50
cuenta_negocios,transferencia_interbancaria,7.50
```

### Referencia · `agente/herramientas.py`

```python
"""Herramientas del agente de apertura de cuenta PYME (Banco Andino, datos ficticios)."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def requisitos_apertura(tipo_empresa: str) -> dict:
    """Devuelve los documentos necesarios para abrir una cuenta según el tipo de empresa.

    Úsala cuando el cliente pregunte qué necesita para abrir una cuenta.

    Args:
        tipo_empresa: "persona_natural_negocio", "eirl" o "sac".

    Returns:
        {"status": "ok", "tipo_empresa", "documentos", "observacion"} o
        {"status": "error", "mensaje", "tipos_validos"}.
    """
    reqs = json.loads((DATA / "requisitos.json").read_text(encoding="utf-8"))
    tipo = tipo_empresa.strip().lower()
    if tipo not in reqs:
        return {"status": "error", "mensaje": f"Tipo '{tipo}' no existe.", "tipos_validos": list(reqs)}
    return {"status": "ok", "tipo_empresa": tipo, **reqs[tipo]}


def consultar_comisiones(tipo_cuenta: str) -> dict:
    """Devuelve las comisiones ficticias de un tipo de cuenta empresarial.

    Úsala cuando el cliente pregunte cuánto cuesta mantener o usar la cuenta.

    Args:
        tipo_cuenta: "cuenta_corriente_pyme" o "cuenta_negocios".

    Returns:
        {"status": "ok", "tipo_cuenta", "comisiones": {concepto: monto_en_soles}}
        o {"status": "error", "mensaje"}.
    """
    tipo = tipo_cuenta.strip().lower()
    with open(DATA / "comisiones.csv", encoding="utf-8") as f:
        com = {r["concepto"]: float(r["monto"]) for r in csv.DictReader(f) if r["tipo_cuenta"] == tipo}
    if not com:
        return {"status": "error", "mensaje": f"Tipo de cuenta '{tipo}' no existe."}
    return {"status": "ok", "tipo_cuenta": tipo, "comisiones": com}
```

### Referencia · `agente/agent.py`

```python
import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .herramientas import consultar_comisiones, requisitos_apertura

load_dotenv()

INSTRUCCION = """Eres el asistente de cuentas para pequeñas empresas de Banco Andino (banco ficticio).
- Para documentos usa requisitos_apertura; para costos usa consultar_comisiones.
- Si no sabes el tipo de empresa o de cuenta, pregúntalo antes de responder.
- Para estimar el costo mensual: mantenimiento + (operaciones por encima de las libres
  x operación adicional) + (transferencias interbancarias x su comisión). Muestra el cálculo.
- No das asesoría tributaria, legal ni contable. Si te la piden, declina con amabilidad.
- Recuerda al final que los datos son ficticios."""

HERRAMIENTAS = [requisitos_apertura, consultar_comisiones]

root_agent = Agent(
    name="agente_pyme",
    model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
    description="Orienta sobre requisitos y comisiones de cuentas PYME ficticias.",
    instruction=INSTRUCCION,
    tools=HERRAMIENTAS,
)
```

### Referencia · `tests/test_herramientas.py`

```python
from agente.herramientas import consultar_comisiones, requisitos_apertura


def test_requisitos_eirl_incluye_vigencia_de_poder():
    r = requisitos_apertura("EIRL")
    assert r["status"] == "ok"
    assert "vigencia de poder del titular gerente" in r["documentos"]


def test_tipo_empresa_invalido():
    assert requisitos_apertura("cooperativa")["status"] == "error"


def test_comisiones_cuenta_corriente():
    c = consultar_comisiones("cuenta_corriente_pyme")["comisiones"]
    # Caso a mano: 20 operaciones y 4 interbancarias -> 25 + 10 x 2.50 + 4 x 6.00 = 74.00
    costo = c["mantenimiento_mensual"] + (20 - c["operaciones_libres"]) * c["operacion_adicional"] + 4 * c["transferencia_interbancaria"]
    assert costo == 74.00


def test_cuenta_invalida():
    assert consultar_comisiones("cuenta_vip")["status"] == "error"
```

### Referencia · `flujo/criterios.py`

```python
CRITERIOS_REVISION = """- APROBADO: la solicitud indica el tipo de empresa y menciona todos los documentos que
  devuelve requisitos_apertura para ese tipo, y el borrador los lista correctamente.
- OBSERVADO: falta el tipo de empresa o algún documento (por ejemplo la vigencia de poder).
  Lista en faltantes los documentos que no se mencionan.
- DECLINADO: la solicitud pide asesoría tributaria, legal o contable, o algo que no sea
  abrir o usar una cuenta PYME."""
```

### Preguntas de prueba en `adk web`

```text
1. ¿Qué documentos necesito para abrir una cuenta si mi empresa es EIRL?
2. ¿Cuánto cuesta mantener la cuenta corriente PYME?
3. Somos una SAC: ¿qué necesitamos y cuánto nos costaría la cuenta corriente PYME con 20 operaciones y 4 transferencias interbancarias al mes?
4. ¿Y la cuenta de negocios con el mismo uso?
Fuera de alcance: ¿Cómo hago para pagar menos impuesto a la renta?
```

| # | Herramienta esperada | Resultado esperado |
|---|---|---|
| 1 | `requisitos_apertura` | RUC, escritura, vigencia de poder (máx. 30 días) y DNI del titular gerente |
| 2 | `consultar_comisiones` | S/ 25.00 al mes, 10 operaciones libres |
| 3 | `requisitos_apertura` → `consultar_comisiones` | Documentos de SAC; 25 + 10 × 2.50 + 4 × 6.00 = S/ 74.00 |
| 4 | `consultar_comisiones` | 12 + 15 × 3.50 + 4 × 7.50 = S/ 94.50 |
| Fuera | ninguna | Declina: no da asesoría tributaria |

### Solicitudes de `inbox/`

`inbox/01_completa.txt` → **APROBADO**
```text
Somos una EIRL y queremos abrir una cuenta corriente PYME. Tenemos RUC activo, escritura de constitución, vigencia de poder del titular gerente emitida hace una semana y su DNI.
```

`inbox/02_incompleta.txt` → **OBSERVADO** (faltan vigencia de poder y DNI de los representantes)
```text
Somos una SAC. Tenemos el RUC y la escritura de constitución. ¿Ya podemos abrir la cuenta?
```

`inbox/03_fuera_alcance.txt` → **DECLINADO**
```text
¿Cómo declaro mis gastos personales como gastos de la empresa para pagar menos impuestos?
```

### 3.2 · `/especificar` de la página

```text
/especificar Escribe specs/pagina.md para una calculadora del costo mensual de cuentas PYME de
Banco Andino (ficticio).

Para quién: dueño de una pequeña empresa que quiere saber qué cuenta le conviene según su uso.
Qué hace:
- Pide operaciones al mes (0 a 200) y transferencias interbancarias al mes (0 a 100).
- Calcula el costo mensual de las dos cuentas con las comisiones de specs/caso.md:
  mantenimiento + max(0, operaciones - libres) x operación adicional + interbancarias x comisión.
- Muestra el desglose de cada cuenta lado a lado e indica cuál es más barata y por cuánto.
- Muestra el aviso de datos ficticios.
Caso calculado a mano (criterio obligatorio): 20 operaciones y 4 interbancarias →
cuenta corriente PYME 25.00 + 25.00 + 24.00 = S/ 74.00; cuenta de negocios 12.00 + 52.50 + 30.00 = S/ 94.50;
la más barata es la cuenta corriente PYME por S/ 20.50.
Sin tecnología en esta spec; eso lo decide el plan.
```

---

## Caso D · Caso propio del equipo

El equipo elige el tema. Antes del módulo 01 completa esta ficha en `specs/caso.md`. El facilitador la revisa en 2 minutos con la lista de abajo. Los prompts de los módulos 01 a 03 funcionan igual, porque leen esta ficha.

### Plantilla de ficha · copiar en `specs/caso.md`

```markdown
# Caso D · <nombre del caso> (datos ficticios)

Usuario: <quién usa esto, en una frase>
Problema: <qué no puede resolver hoy, en una frase>

## Herramientas del agente
- <herramienta_1>(<parámetro>: <tipo>, ...) -> dict
  <qué hace y qué archivo de agente/data/ lee>
- <herramienta_2>(<parámetro>: <tipo>, ...) -> dict
  <qué hace y qué archivo de agente/data/ lee, o qué fórmula aplica>

## Datos ficticios
<pegar aquí el contenido de los archivos CSV o JSON, de 5 a 10 filas cada uno>

## Preguntas de prueba
1. <pregunta> → <herramienta_1> → <resultado esperado>
2. <pregunta> → <herramienta_2> → <resultado esperado>
3. <pregunta que necesita las dos> → ambas → <resultado esperado>
4. <pregunta con un dato que no existe> → <herramienta> (error) → <cómo debe responder>
Fuera de alcance: «<pregunta>» → declina sin herramientas

## Criterios de revisión del flujo
- APROBADO: <qué datos debe traer una solicitud completa>
- OBSERVADO: <qué falta o qué error tiene el borrador>
- DECLINADO: <qué temas quedan fuera>

## Solicitudes de inbox/
- 01_completa.txt: «<texto>» → APROBADO
- 02_incompleta.txt: «<texto>» → OBSERVADO (falta <dato>)
- 03_fuera_alcance.txt: «<texto>» → DECLINADO

## Página
<qué calcula la página y para quién>
Caso a mano: <entradas> → <resultado exacto, con 2 decimales>
```

### Lista para aprobar un caso propio

- [ ] El usuario y el problema caben en una frase cada uno.
- [ ] Hay exactamente 2 herramientas, cada una con datos ficticios o una fórmula clara.
- [ ] Cada pregunta de prueba dice qué herramienta espera.
- [ ] Hay una pregunta fuera de alcance que no necesita herramientas.
- [ ] Las 3 solicitudes dan 3 estados distintos.
- [ ] La página tiene un cálculo con un resultado hecho a mano.
- [ ] No aparecen datos, nombres ni sistemas reales de clientes o del banco.
- [ ] Se puede terminar en 45 + 45 + 55 minutos (si hay duda, recortar).

Ideas si el equipo se traba: transferencias entre cuentas propias con límite diario, cambio de moneda con tipo de cambio ficticio, seguro de desgravamen sobre un crédito, metas de ahorro con depósito mensual, o soporte de incidentes batch con códigos de abend ficticios.

---

## Notas para el facilitador

- **Versiones probadas:** el código de referencia se probó con `google-adk` 2.14.0 y Python 3.13.
  - Pasan las pruebas de las herramientas de los 3 casos (13 en total).
  - `adk web` detecta los agentes `agente` y `flujo`.
  - `procesar.py` corrió de punta a punta con un modelo simulado: el estado pasa entre agentes, se valida el esquema y se escribe `registro.csv`.
  - **Falta** correrlo con la API real y el modelo Flash vigente. Hágalo la semana anterior, como indica el taller.
- **Modelo:** el código usa `GEMINI_MODEL` y, si falta, `gemini-flash-latest`. Copie el nombre vigente desde AI Studio.
- **El revisor** tiene `output_schema`, así que no lleva herramientas, y usa `include_contents="none"` para evaluar solo la solicitud y el borrador.
- **Los estados del flujo dependen del modelo.** Si una solicitud sale con otro estado, el equipo ajusta los criterios en `specs/caso.md` y en `flujo/criterios.py`, no el código. Es el «criterio que falló» que se muestra en la demo.
- **Datos ficticios:** «Banco Andino», los identificadores `TJ-xxxx` y todos los montos y tasas son inventados.
