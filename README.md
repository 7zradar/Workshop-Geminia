# Workshop QA con Gemini y Antigravity

Tres horas para desarrolladores de TCS. Construye un agente QA, reutilízalo en una automatización con un segundo agente revisor y crea un dashboard mediante vibe coding guiado por specs y skills.

El agente es de QA. La calculadora ficticia de cuenta PYME es la aplicación que revisa. La demo parte con dos defectos verificables y permite aplicar la corrección al código real, disparar otra ejecución y comparar sus resultados.

## Participante: prepara todo con un comando antes del taller

Descarga el [ZIP de esta rama](https://github.com/7zradar/Workshop-Geminia/archive/refs/heads/codex/qa-workshop.zip), extráelo y abre PowerShell en la carpeta que contiene preparar-workshop.ps1. Necesitas Antigravity con sesión iniciada, Python 3.12 y Node 22 o superior. Si falta Python o Node, el script indica qué debe instalar TI; no instala herramientas del sistema. Git no es necesario al usar el ZIP.

```powershell
powershell -NoProfile -File .\preparar-workshop.ps1
```

Espera **PREPARACION COMPLETA** y abre la carpeta indicada, `practica/equipo-01`, en Antigravity. El comando crea el kit inicial, prepara `.venv`, instala las dependencias y verifica ADK, las tres skills y las pruebas locales. El kit nuevo muestra 2/4 y 50 % por el bug intencional. No pide una API key ni llama a Gemini. Los agentes y el dashboard quedan por construir con los prompts del HTML.

Si se interrumpe, repite el mismo comando. Conserva código, contratos, skills y `.env` de un kit identificado, agrega solo archivos ausentes y reutiliza dependencias cuando siguen válidas. Para otra práctica agrega `-Equipo equipo-02`. Una carpeta previa sin la marca del preparador se conserva y requiere elegir otro nombre. La preparación necesita acceso al repositorio de paquetes Python; si TI restringe scripts o descargas, comparte el error antes del evento. El script no cambia la política de PowerShell.

**Configura GOOGLE_API_KEY una sola vez en el `.env` de la práctica después de construir el primer agente y antes de su primera ejecución con Gemini.** Los dos agentes y RAG reutilizan esa configuración. No necesitas activar el entorno manualmente: los siguientes comandos usan el entorno ya preparado.

| Momento del taller | Comando desde la práctica |
|---|---|
| Primera ejecución del agente construido | `.\taller.ps1 agente` |
| Ejecutar QA y revisor construidos | `.\taller.ps1 flujo` |
| Iniciar vigilancia para los bloques 2 y 3 | `.\taller.ps1 automatizar` |
| Reto del revisor | `.\taller.ps1 revisor` |

En el bloque 3 abre http://127.0.0.1:8767/ usando el servidor que ya está funcionando. El HTML mantiene la agenda de 180 minutos. Specs, skills y vibe coding se usan desde el primer módulo. La [spec del entorno](specs/entorno.md) detalla el comportamiento del preparador.

## Facilitador: abrir la demostración

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

WORKSHOP_GEMINI.html es autocontenido. Para compartir la presentación, descarga ese archivo con el control Download raw file de GitHub y ábrelo con doble clic. Los estilos, las tres experiencias con sus 17 pasos y la Experiencia 4 opcional de RAG están integrados en el HTML.

## Facilitador: activar Gemini en la referencia

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

La solución de este repositorio sirve como referencia del facilitador. Cada participante utiliza la preparación de un comando indicada al inicio y abre su práctica en Antigravity. El kit trae el motor, contratos, infraestructura, workflow y skills. Los equipos redactan sus specs e implementan agente/, flujo/ y pagina/. La clave se configura después de construir el primer agente. El archivo .env de la solución no se copia al kit.

La [guía paso a paso](Guia_paso_a_paso_QA.md) detalla carpetas, terminales, acciones y resultados para realizar las tres experiencias. El [guion breve](Taller_QA_Gemini.md) resume los tiempos y la [presentación](WORKSHOP_GEMINI.html) contiene los prompts copiables.

El segundo reto se ejecuta con `.\taller.ps1 revisor`, que presenta al revisor evidencia real de fallas y un diagnóstico de éxito intencionalmente inconsistente. Requiere Gemini configurado y el flujo implementado, y guarda el resultado en salida/reto-revisor.json.

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

## Experiencia 4 opcional: contexto con RAG

El agente QA tiene una tercera herramienta, `buscar_contexto`, que recupera fragmentos de `conocimiento/` (reglas de negocio, historial de defectos y guía de severidad, todo ficticio). Cada hallazgo cita sus fuentes en `sources` y el reporte guarda los fragmentos recuperados en `context`. La búsqueda es local y determinista, no consume peticiones de Gemini. El reporte se rechaza si cita una fuente que no se recuperó en esa ejecución. Las pruebas siguen determinando el veredicto. La especificación está en specs/rag.md y la experiencia en la presentación, con prompts y pasos. Cambiar un documento de `conocimiento/` genera un reporte nuevo por contenido y modo.

La agenda base conserva sus 180 minutos. Esta extensión añade 20 minutos si se imparte completa. La práctica base construye primero dos herramientas; la solución de referencia ya incluye las tres. La guía independiente desarrolla también los cinco pasos opcionales. En ADK Web las consultas comparten la instantánea de conocimiento y acumulan citas durante la ejecución. El workflow de GitHub se activa también con cambios en `conocimiento/`.
