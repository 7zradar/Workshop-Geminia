# Walkthrough de validación

Validación local del 11 de noviembre de 2026. Python 3.12, Node 24 y google-adk 2.14.0.

## Evidencia ejecutada

| Criterio | Comprobación | Resultado |
|---|---|---|
| W1 | Suma de agenda y duración de los pasos | 180 minutos, bloques de 45, 45 y 55 |
| W2, P8 | Recorrido en navegador de los 17 pasos | Specs, skills, planes, construcción, verificación y retos presentes |
| W3 | Validador de skills | Tres SKILL.md válidos |
| A1 | Runner sobre versión defectuosa | QA-02 obtiene 50 frente a 25, QA-03 obtiene 99 frente a 74, 50 % aprobado |
| A2 | Runner sobre versión corregida | Cuatro pruebas aprobadas, 100 % |
| A4 | Reporte con hallazgo inventado | Rechazado por validación de correspondencia |
| A5 | Modo Gemini sin clave | Error explícito antes de llamar al modelo |
| A6, W8 | Revisión de interfaz y JSON | Modo evidencia identificado como pruebas reales y diagnóstico local |
| F1, P2 | Botón de corrección escribe el archivo real | Vigilancia produce reporte nuevo con trigger cambio |
| F2 | Repetir contenido y modo | Un reporte por identidad |
| F3 | Cambio durante ejecución retenida | Se conservan las dos instantáneas y el último reporte corresponde a la corrección |
| F4 | Motor JavaScript inválido | Error y último reporte válido conservado |
| F5 | Runtime de dos agentes ADK con modelo local inyectado | Ambas herramientas se ejecutan y el revisor produce salida estructurada |
| P1, P5 | Contadores y filtro en navegador | 4 casos globales y 2 visibles al filtrar fallidos |
| P3 | Importar reporte válido | Valores y hallazgos coinciden con el archivo |
| P4 | Importar archivo inválido | Error visible y datos anteriores conservados |
| P7 | Tamaños de escritorio y 375 px | Sin desbordamiento horizontal |
| P7 | Navegación por teclado | Tab desde ejecutar QA llega al filtro y el foco es visible |
| ADK Web | GET list-apps | Reconoce agente y flujo |
| Kit inicial | Preparación y repetición sobre el mismo destino | Inicia con bug y evita sobrescribir el trabajo existente |
| P9 | HTML copiado a una carpeta temporal y analizado | Estilos, contenido y scripts integrados, sin recursos externos obligatorios |
| P8, P9 | Recorrido del HTML integrado en la vista HTTP | Tres tarjetas y 17 pasos accesibles |

`python -m pytest -q` termina con **14 passed**. Las advertencias de SequentialAgent corresponden a la API de compatibilidad de la versión fijada y están documentadas en README.md.

## Capturas

- capturas/dashboard-con-fallas.jpg muestra 2 aprobadas, 2 fallidas y 50 %.
- capturas/dashboard-corregido.jpg muestra 4 aprobadas, 0 fallidas y 100 %.
- capturas/presentacion-agente.jpg muestra la spec, instrucciones y prompt copiable de la primera experiencia.
- capturas/presentacion-autocontenida.jpg muestra las tres tarjetas después de integrar los recursos en el HTML.

## Validaciones pendientes

- Llamada a Gemini real. El usuario configurará la clave cuando revise la demo. El ensayo ADK utiliza un modelo local inyectado y no acredita una llamada a la API.
- Ejecución remota en GitHub Actions. Se entregó el workflow para push y ejecución manual. Requiere subir el proyecto y configurar secretos y variables en GitHub.

El dashboard abre inicialmente la versión defectuosa para que la demostración tenga un antes y después. La ausencia de fallas de la versión corregida se refiere a los cuatro casos ejecutados.
