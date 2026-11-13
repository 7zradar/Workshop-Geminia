# Agente QA con Gemini y Antigravity

Para realizar cada paso con comandos, carpetas, verificaciones y recuperación, utiliza la [guía paso a paso](Guia_paso_a_paso_QA.md).

## Propósito y materiales

Workshop práctico de 180 minutos para desarrolladores. Cada equipo construye un agente QA, un flujo con un revisor y un dashboard. SDD y skills se aplican durante las tres experiencias.

La aplicación bajo prueba es la calculadora ficticia del paquete de casos. El motor inicial cobra todas las operaciones, aunque las primeras diez son gratuitas. El agente debe descubrir y explicar las diferencias con evidencia. La solución completa sirve al facilitador y el kit de practica/ a los participantes.

## Preparación previa

Cada participante ejecuta `powershell -NoProfile -ExecutionPolicy Bypass -File .\preparar-workshop.ps1` antes del evento. Comprueba Python y Node, prepara el kit y sus dependencias y verifica las skills y pruebas locales sin pedir la clave. Si faltan herramientas del sistema, informa qué instalar con TI. El participante abre la carpeta indicada en Antigravity y construye los entregables con el HTML. Configura la clave una vez, después de construir el agente, antes de su primera ejecución con Gemini.

Como facilitador, usa iniciar.ps1 para ensayar la solución completa con tu propia configuración y comprobar una llamada real antes del evento. Conserva esa referencia para recuperar un equipo que se retrase. Specs, skills y vibe coding se aplican desde el módulo 1.

Lleva las dos versiones del motor, la spec y los casos. La presentación HTML contiene los prompts completos para copiar durante la sesión.

## Apertura, 15 minutos

Explica qué hace el agente QA y qué aplicación revisa. Ejecuta el caso QA-03 y relaciona 74 esperado con 99 obtenido. Presenta el ciclo spec, plan, tareas, código y verificación. Abre una skill y muestra su name, description y procedimiento. Comprueba el entorno y abre el kit del equipo en Antigravity.

## Experiencia 1, 45 minutos

1. Spec, 6 minutos. Usa /especificar para definir entradas, herramientas y salida del agente. Revisa los criterios de specs/agente-qa.md.
2. Skill, 4 minutos. Edita verificar/SKILL.md para comprobar las huellas source_hash y contract_hash junto con los datos de cada falla. Muestra su aplicación.
3. Plan, 4 minutos. Usa Planning o /plan. Revisa herramientas, agente y verificación. El kit provee qa_core.py y el runner.
4. Construcción, 18 minutos. Implementa una tarea por vez. El agente exporta create_agent(evidence, model=None) y root_agent. Usa leer_criterios y ejecutar_pruebas. Esta última guarda evidencia en el estado.
5. Verificación, 11 minutos. Configura la clave una vez e inicia `.\taller.ps1 agente`. En ADK Web observa las llamadas. Contrasta QA-02 y QA-03 con el contrato. Distingue llamada real a Gemini de ensayo local.
6. Reto opcional, 2 minutos. Solo si el equipo va a tiempo; si no, es margen. Como extensión agrega 11 operaciones y 0 transferencias, esperado 27.50. Registra primero el criterio. Con cinco casos, el resultado inicial es 40 % y el corregido 100 %.

Entrega de este bloque con spec, plan, agente y evidencia de herramientas.

## Experiencia 2, 45 minutos

1. Spec, 5 minutos. Define disparadores, entrada, segundo agente, resultado y errores. Repetir un contenido no debe duplicar el historial.
2. Plan, 3 minutos. Copia plantillas/flujo/agent.py a flujo/agent.py. La plantilla trae los imports, la interfaz de procesar.py y los modelos Analysis y Review de flujo/modelos.py. Planifica la instrucción del revisor y la secuencia.
3. Construcción, 15 minutos. Completa los TODO de la plantilla para conectar QA y revisor. El revisor recibe diagnostico y evidencia y devuelve decision y observations. Ejecuta `.\taller.ps1 flujo` con la configuración del bloque anterior.
4. Automatización, 12 minutos. Inicia `.\taller.ps1 automatizar` en el puerto 8767 y comprueba la vigilancia. Abre el JSON con Antigravity. Corrige operacionesCobradas con Math.max(0, operaciones - 10). Guardar el archivo dispara otra revisión. Conserva el servidor para el dashboard del bloque 3.
5. Verificación, 8 minutos. Compara 50 % y 100 % con el contrato base, o 40 % y 100 % con cinco casos. La huella de fuente cambia y la del mismo contrato permanece. Repite para comprobar identidad.
6. Reto opcional, 2 minutos. Solo si el equipo va a tiempo. Ejecuta `.\taller.ps1 revisor` con Gemini configurado. Comprueba OBSERVADO ante un diagnóstico que declare éxito cuando un caso falla.

Entrega de este bloque con dos agentes, ejecución automática y reporte JSON.

## Pausa, 10 minutos

## Experiencia 3, 55 minutos

1. Spec, 7 minutos. Usa el JSON real para definir contador, porcentaje, casos, filtros, diagnóstico, revisión y traza.
2. Plan, 5 minutos. Copia plantillas/pagina/ (HTML y CSS listos) a pagina/. Divide validación, renderizado, controles y verificación de pagina/app.js. Revisa las rutas disponibles en servidor.py.
3. Construcción, 25 minutos. Usa /implementar para construir pagina/app.js sobre los id del HTML. Renderiza los valores importados como texto. Distingue el origen del reporte.
4. Verificación, 15 minutos. Comprueba antes y después, filtro, archivo inválido, teclado y ancho móvil. Conserva evidencia en el walkthrough.
5. Reto y demo, 3 minutos. La mejora (filtro por ID o comparación de reportes) es opcional; preparar la demo no.

Entrega de este bloque con dashboard conectado al reporte y walkthrough.

## Cierre, 10 minutos

Selecciona equipos según el tiempo disponible. Cada demo dura dos minutos y muestra la spec, una skill aplicada, el defecto, el cambio automático, el revisor y el dashboard corregido. Usa el resto del tiempo para revisar cómo cada evidencia respalda un criterio.

## Guía de recuperación

- Si falta Gemini, usa modo evidencia para continuar con pruebas reales. Identifica la validación del modelo como pendiente.
- Si el agente omite una herramienta, revisa la instrucción y su docstring y repite el criterio.
- Si cambia la spec para ocultar un fallo, vuelve al requisito acordado y corrige la implementación.
- Si una salida falla su esquema, conserva el reporte anterior y muestra el error antes de reintentar.
- Si el equipo se retrasa, compara el componente con la solución del facilitador y conserva sus specs y cambios.

## Comprobación de la entrega

| Requisito | Evidencia |
|---|---|
| SDD | Specs, planes y verificación por criterio |
| Skills | Tres SKILL.md y una modificación durante el ejercicio |
| Agente | Dos herramientas con ejecución real |
| Automatización y agente adicional | Vigilancia, QA y revisor |
| Vibe coding | Construcción asistida desde el módulo 1, guiada por specs y skills |
| Tres horas | 15 + 45 + 45 + 10 + 55 + 10 = 180 |
| Experiencia 4 opcional | RAG local con `buscar_contexto`, 20 minutos fuera de los 180 |
