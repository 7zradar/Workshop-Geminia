# Automatización QA

## Proceso
Inicio manual, cambio local en app/calculadora.mjs o push en GitHub Actions. El flujo toma una instantánea del motor y de los criterios, ejecuta el mismo agente QA y añade un revisor. El revisor recibe el diagnóstico y todos los resultados de pruebas. Su salida estructurada tiene decision VALIDADO u OBSERVADO y observaciones.

## Integridad
Cada reporte usa un ID derivado del contenido del motor, los criterios y el modo de ejecución. Repetir el contenido conserva un solo registro y permite volver a intentarlo tras un error. Las escrituras son atómicas. Las ejecuciones locales se serializan. Un cambio durante una ejecución queda pendiente para la siguiente. Un error conserva el último reporte correcto y queda visible en el estado del servidor.

## Criterios
| ID | Acción | Esperado |
|---|---|---|
| F1 | Cambiar el código con vigilancia activa | Nuevo reporte automático con trigger cambio |
| F2 | Repetir la misma versión y modo | Historial sin duplicados |
| F3 | Cambiar la fuente durante una ejecución | Cada reporte identifica su instantánea y se procesa el cambio pendiente |
| F4 | Fallar autenticación o Node | Error visible, último reporte conservado |
| F5 | Revisar reporte Gemini | Dos agentes secuenciales y salida del revisor validada |
| F6 | Ejecutar GitHub Actions | Artefacto con JSON e historial, claves desde secrets |
| F7 | Correr modo evidencia | Revisión determinista de consistencia identificada como local |
