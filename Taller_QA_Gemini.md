# Agente QA con Gemini y Antigravity

## Propósito y materiales

Workshop práctico de 180 minutos para desarrolladores. Cada equipo construye un agente QA, un flujo con un revisor y un dashboard. SDD y skills se aplican durante las tres experiencias.

La aplicación bajo prueba es la calculadora ficticia del paquete de casos. El motor inicial cobra todas las operaciones, aunque las primeras diez son gratuitas. El agente debe descubrir y explicar las diferencias con evidencia. La solución completa sirve al facilitador y el kit de practica/ a los participantes.

## Preparación previa

Ejecuta iniciar.ps1, comprueba Node y Python, configura la clave en .env y ensaya una llamada real con Gemini antes del evento. Verifica que Antigravity descubre las tres skills. Crea un kit por equipo con scripts/preparar_practica.py y prepara el entorno de cada carpeta. Conserva la solución completa para recuperar un equipo que se retrase.

Lleva las dos versiones del motor, la spec y los casos. La presentación HTML contiene los prompts completos para copiar durante la sesión.

## Apertura, 15 minutos

Explica qué hace el agente QA y qué aplicación revisa. Ejecuta el caso QA-03 y relaciona 74 esperado con 99 obtenido. Presenta el ciclo spec, plan, tareas, código y verificación. Abre una skill y muestra su name, description y procedimiento. Comprueba el entorno y abre el kit del equipo en Antigravity.

## Experiencia 1, 45 minutos

1. Spec, 8 minutos. Usa /especificar para definir entradas, herramientas y salida del agente. Revisa los criterios de specs/agente-qa.md.
2. Skill, 4 minutos. Edita verificar/SKILL.md para exigir ID y evidencia de cada falla. Muestra su aplicación.
3. Plan, 5 minutos. Usa Planning o /plan. Revisa herramientas, agente y verificación. El kit provee qa_core.py y el runner.
4. Construcción, 15 minutos. Implementa una tarea por vez. El agente exporta create_agent(evidence, model=None) y root_agent. Usa leer_criterios y ejecutar_pruebas. Esta última guarda evidencia en el estado.
5. Verificación, 10 minutos. En adk web observa las llamadas. Contrasta QA-02 y QA-03 con el contrato. Distingue llamada real a Gemini de ensayo local.
6. Reto, 3 minutos. Agrega 11 operaciones y 0 transferencias, esperado 27.50. Registra primero el criterio.

Entrega de este bloque con spec, plan, agente y evidencia de herramientas.

## Experiencia 2, 45 minutos

1. Spec, 8 minutos. Define disparadores, entrada, segundo agente, resultado y errores. Repetir un contenido no debe duplicar el historial.
2. Plan, 5 minutos. Reutiliza create_agent. Define modelos Analysis y Review y create_pipeline(evidence, model) según las interfaces de procesar.py.
3. Construcción, 15 minutos. Conecta QA y revisor. El revisor recibe diagnostico y evidencia y devuelve decision y observations. Ejecuta python procesar.py --mode gemini.
4. Automatización, 10 minutos. Inicia servidor.py y comprueba la vigilancia. Corrige operacionesCobradas con Math.max(0, operaciones - 10). Guardar el archivo dispara otra revisión. El workflow de GitHub está preparado como alternativa reproducible.
5. Verificación, 5 minutos. Compara 50 % y 100 %. La huella de fuente cambia y la del contrato permanece. Repite para comprobar identidad.
6. Reto, 2 minutos. Comprueba que el revisor observe un diagnóstico que declare éxito cuando un caso falla.

Entrega de este bloque con dos agentes, ejecución automática y reporte JSON.

## Pausa, 10 minutos

## Experiencia 3, 55 minutos

1. Spec, 10 minutos. Usa el JSON real para definir contador, porcentaje, casos, filtros, diagnóstico, revisión y traza.
2. Plan, 8 minutos. Divide validación, renderizado, controles y verificación. Revisa las rutas disponibles en servidor.py.
3. Construcción, 20 minutos. Usa /implementar para construir HTML, CSS y JavaScript. Renderiza los valores importados como texto. Distingue el origen del reporte.
4. Verificación, 12 minutos. Comprueba antes y después, filtro, archivo inválido, teclado y ancho móvil. Conserva evidencia en el walkthrough.
5. Reto, 5 minutos. Añade un filtro por ID o una comparación de reportes, con su spec y criterio.

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
| Vibe coding | Dashboard construido desde spec |
| Tres horas | 15 + 45 + 45 + 10 + 55 + 10 = 180 |
