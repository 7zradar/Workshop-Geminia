# Workshop QA con Gemini y Antigravity

Tres horas para desarrolladores de TCS. Construye un agente QA, reutilízalo en una automatización con un segundo agente revisor y crea un dashboard mediante vibe coding guiado por specs y skills.

El agente es de QA. La calculadora ficticia de cuenta PYME es la aplicación que revisa. La demo parte con dos defectos verificables y permite aplicar la corrección al código real, disparar otra ejecución y comparar sus resultados.

## Abrir la demostración

Instala Python 3.12 y Node 22 o superior. En PowerShell, desde la carpeta del repositorio ejecuta lo siguiente.

```powershell
.\iniciar.ps1
```

El script prepara el entorno cuando hace falta y arranca la demo en estas direcciones.

- [Dashboard](http://127.0.0.1:8765/)
- [Presentación](http://127.0.0.1:8765/presentacion)

Si la política de PowerShell impide ejecutar el script, puedes iniciar directamente con Python.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe servidor.py
```

El modo inicial es **evidencia**. Ejecuta las pruebas Node reales y genera un diagnóstico local. El dashboard identifica este modo en cada reporte. También puedes abrir WORKSHOP_GEMINI.html o pagina/index.html con doble clic. La presentación funciona como archivo local y el dashboard muestra un ejemplo guardado y permite importar JSON.

## Activar Gemini

1. Copia .env.example a .env y configura GOOGLE_API_KEY.
2. Revisa GEMINI_MODEL con tu cuenta de AI Studio. El valor inicial usa el alias gemini-flash-latest.
3. Inicia `.\iniciar.ps1 -Modo gemini`, o selecciona Gemini en el dashboard y ejecuta QA.

La clave permanece en el backend. Los dos agentes ADK se ejecutan en modo Gemini. El primero consulta criterios y ejecuta pruebas. El segundo recibe evidencia y diagnóstico y devuelve una revisión estructurada.

Para inspeccionar directamente el agente en ADK Web, activa tu entorno y ejecuta `adk web` desde la raíz. Elige agente para la primera experiencia o flujo para los dos agentes. Pide que revise el motor actual y abre Events para ver las herramientas.

## Guion para mostrar el producto en cinco minutos

1. Abre la presentación y explica que specs y skills guían la construcción.
2. Abre el dashboard y pulsa Restaurar bug del ejercicio si necesitas volver al inicio.
3. Muestra 2 aprobadas, 2 fallidas y 50 %. QA-02 exige 25 y obtiene 50. QA-03 exige 74 y obtiene 99.
4. Abre la evidencia y la traza. Identifica el modo de ejecución.
5. Comprueba que la vigilancia está activa y pulsa Aplicar corrección. Este control copia la solución pedagógica al archivo app/calculadora.mjs. También puedes editarlo en Antigravity.
6. Espera el reporte con disparador cambio. Muestra 4 aprobadas, 0 fallidas y 100 %.
7. En el historial compara las huellas del código. Exporta el JSON si deseas conservar la evidencia.

La demostración local funciona antes de configurar Gemini. Las llamadas al modelo requieren la clave y están sujetas a sus tiempos y cuotas.

## Realizar el workshop

La solución de este repositorio sirve como referencia del facilitador. Para que cada equipo construya sus entregables desde un kit inicial, genera una carpeta independiente.

```powershell
python scripts/preparar_practica.py --equipo equipo-01
```

Abre practica/equipo-01 en Antigravity. El kit trae el motor, contratos, infraestructura, workflow y skills. Los equipos redactan sus specs e implementan agente/, flujo/ y pagina/. Configura el entorno y la clave en la carpeta de práctica antes de la sesión. El archivo .env de la solución no se copia al kit.

El guion detallado está en [Taller_QA_Gemini.md](Taller_QA_Gemini.md) y los pasos utilizables en [WORKSHOP_GEMINI.html](WORKSHOP_GEMINI.html).

## Specs y skills

- specs/workshop.md define objetivos y agenda de 180 minutos.
- specs/aplicacion.md y contratos/casos.json fijan las expectativas de negocio.
- specs/agente-qa.md, specs/flujo.md y specs/pagina.md definen los entregables.
- specs/plan.md relaciona implementación y verificación.
- .agents/skills/especificar, implementar y verificar contienen los SKILL.md para Antigravity.
- AGENTS.md registra convenciones e invariantes del proyecto.

Los criterios claros se mantienen al corregir un defecto. Un cambio de requisito se registra en la spec antes de modificar la implementación.

## Automatización

El servidor observa el contenido de app/calculadora.mjs y sus contratos. Captura una instantánea estable para cada ejecución y serializa el trabajo. Los reportes se guardan en salida/reportes/ y el último en salida/ultimo.json. La identidad depende del contenido y del modo, por lo que repetir una versión conserva un registro por combinación. Ante un error se conserva el último reporte válido y se muestra el error.

También puedes ejecutar por terminal.

```powershell
python procesar.py --mode evidencia
python procesar.py --mode gemini
python procesar.py --mode evidencia --fail-on-defects
```

El exit code habitual es 0 si el reporte se generó, 1 con --fail-on-defects cuando existen defectos y 2 ante un error de infraestructura o del modelo.

El workflow .github/workflows/qa.yml se dispara con cambios de código o manualmente. Usa GOOGLE_API_KEY desde secrets y GEMINI_MODEL desde variables. QA_MODE permite elegir evidencia o gemini en los pushes. Conserva salida/ como artefacto incluso cuando las pruebas detectan defectos. La ejecución en GitHub requiere subir estos archivos a un repositorio con Actions habilitado.

## Verificar

```powershell
python -m pytest -q
node scripts/ejecutar-pruebas.mjs
```

El runner del motor termina con exit code 1 en la versión inicial porque contiene dos fallas intencionales. Las pruebas de infraestructura usan carpetas temporales y comprueban ambas versiones, identidad, persistencia, disparador por cambios y el runtime de los dos agentes con un modelo local inyectado. Este último comprueba integración ADK sin llamar a la API.

Python 3.12 y google-adk 2.14.0 son la base de esta entrega. El pipeline conserva SequentialAgent para seguir la estructura del material original y la versión fijada. ADK lo marca como obsoleto en favor de Workflow. Una actualización del SDK debe revisar esta integración y su prueba.

La verificación contra Gemini real queda pendiente hasta configurar la clave. La suite de cuatro casos cubre el motor de cálculo. La interfaz y el reporte se verifican por separado.

## Procedencia

Adaptación del repositorio Workshop-Geminia y del paquete de casos de las compañeras del equipo. El documento original se conserva como material de referencia. Los datos bancarios son ficticios.

Fuentes técnicas consultadas.

- [Skills de Antigravity](https://antigravity.google/docs/skills)
- [Migración de workflows a skills](https://antigravity.google/docs/migration/workflows-to-skills)
- [Inicio con ADK Python](https://adk.dev/get-started/python/)
- [Flujos secuenciales ADK](https://adk.dev/agents/workflow-agents/sequential-agents/)
