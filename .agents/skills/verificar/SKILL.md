---
name: verificar
description: Verifica agente, automatización o dashboard QA contra sus specs y reúne evidencia reproducible.
---

# Verificar

Lee los criterios de la spec indicada. Usa `python -m pytest -q` para infraestructura y `node scripts/ejecutar-pruebas.mjs` para el motor. Un exit code 1 del runner indica casos de negocio fallidos y puede ser el resultado esperado de la versión defectuosa.

Para el flujo verifica repetición, cambio automático y persistencia. Para la página comprueba importación de JSON, filtro de fallos, teclado y ancho móvil. Presenta una tabla con criterio, evidencia y estado. Conserva esperado y obtenido por cada falla.

Distingue pruebas locales, validación de integración ADK y llamada a Gemini real. Registra toda validación pendiente. Una captura acompaña los resultados ejecutables y la traza.
