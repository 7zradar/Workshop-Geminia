# Plan de implementación

Plan derivado de la propuesta de tres horas aprobada en esta conversación. Caso QA sobre el motor ficticio del paquete original. La API key será configurada por el usuario al terminar.

| Tarea | Archivos | Verificación |
|---|---|---|
| T1 | specs/, .agents/skills/, AGENTS.md | Criterios completos y validador de skills |
| T2 | contratos/, app/, demo/, scripts/ejecutar-pruebas.mjs | Runner detecta bug y acepta corrección |
| T3 | agente/, flujo/, qa_core.py | Herramientas, reporte y dos agentes |
| T4 | procesar.py, servidor.py, .github/workflows/qa.yml | Disparo automático, identidad y persistencia |
| T5 | pagina/, WORKSHOP_GEMINI.html, presentacion/ | QA visual, importación y prompts |
| T6 | tests/, README.md, iniciar.ps1, Taller_QA_Gemini.md | Pruebas integradas y guion de demostración |

## Estado
T1 a T6 implementadas y verificadas localmente. Pasan 13 pruebas de infraestructura. Las tres skills pasan su validador. La presentación y el dashboard se comprobaron en navegador, incluyendo el cambio automático de 50 % a 100 %.

La validación con Gemini real requiere la clave que aportará el usuario. El workflow de GitHub está preparado y su ejecución remota queda pendiente de subir los cambios y configurar el repositorio. El detalle de evidencia está en specs/verificacion.md.
