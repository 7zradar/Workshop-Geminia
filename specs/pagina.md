# Dashboard QA

## Usuario
Facilitador, participantes y responsables que quieren ver si el agente detecta y documenta una regresión.

## Experiencia
Vista de resultados con total de pruebas, aprobadas, fallidas y porcentaje. Casos filtrables con esperado, obtenido y criterio. Diagnóstico, revisión y traza consultables. Historial de versiones. El modo evidencia y Gemini aparecen identificados. Se puede ejecutar QA, activar la vigilancia y aplicar la corrección pedagógica al archivo real. El panel incluye una calculadora pequeña para reproducir el cálculo.

La página abre también como archivo local y permite importar un reporte JSON. Los controles que requieren servidor explican cómo iniciarlo. Los errores de red o importación son visibles. Todo contenido de reportes se renderiza como texto.

## Criterios
| ID | Acción | Esperado |
|---|---|---|
| P1 | Cargar 4 casos con 2 fallos | 50 %, dos aprobados y dos fallidos |
| P2 | Aplicar corrección con vigilancia | 100 % tras ejecución automática y traza nueva |
| P3 | Importar JSON exportado | Mismos resultados del servidor |
| P4 | Importar JSON inválido | Mensaje de error y datos anteriores conservados |
| P5 | Filtrar fallos | Solo casos fallidos, contadores globales conservados |
| P6 | Revisar modo | Ningún resultado local se presenta como Gemini |
| P7 | Navegar con teclado y ancho de 375 px | Controles utilizables y sin desbordamiento horizontal |
| P8 | Abrir presentación | Pasos completos de agente, flujo y vibe coding, prompts copiables |
| P9 | Copiar solo WORKSHOP_GEMINI.html a una carpeta vacía y abrirlo | Tres experiencias con 17 pasos y una cuarta opcional con 5 pasos, con estilos y contenido integrados |
