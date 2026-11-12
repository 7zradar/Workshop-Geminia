# Plan de implementación

Plan derivado de la propuesta de tres horas aprobada en esta conversación. Caso QA sobre el motor ficticio del paquete original. La API key será configurada por el usuario al terminar.

| Tarea | Archivos | Verificación |
|---|---|---|
| T1 | specs/, .agents/skills/, AGENTS.md | Criterios completos y validador de skills |
| T2 | contratos/, app/, demo/, scripts/ejecutar-pruebas.mjs | Runner detecta bug y acepta corrección |
| T3 | agente/, flujo/, qa_core.py | Herramientas, reporte y dos agentes |
| T4 | procesar.py, servidor.py, .github/workflows/qa.yml | Disparo automático, identidad y persistencia |
| T5 | pagina/, WORKSHOP_GEMINI.html | QA visual, importación y prompts |
| T6 | tests/, README.md, iniciar.ps1, Taller_QA_Gemini.md | Pruebas integradas y guion de demostración |
| T7 | WORKSHOP_GEMINI.html, tests/, README.md | Presentación autocontenida comprobada como único archivo en una carpeta vacía |
| T8 | Guia_paso_a_paso_QA.md, WORKSHOP_GEMINI.html, README.md, scripts/probar_revisor.py, qa_core.py, agente/, flujo/, tests/ | Recorrido de las tres experiencias, guía operativa, revisor aislado y totales del quinto caso |

## Estado
T1 a T8 implementadas y verificadas localmente. Pasan 16 pruebas de infraestructura. Las tres skills pasan su validador. La presentación y el dashboard se comprobaron en navegador, incluyendo el cambio automático de 50 % a 100 %. La presentación integra estilos y contenido en un único HTML. La guía independiente desarrolla los 17 pasos y sus tres retos.

La validación con Gemini real requiere la clave que aportará el usuario. El workflow de GitHub está preparado para configurar y ensayar en el repositorio. El detalle de evidencia está en specs/verificacion.md.
