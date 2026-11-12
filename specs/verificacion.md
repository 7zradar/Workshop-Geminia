# Walkthrough de validación

Validación local del 11 de noviembre de 2026, ampliada el 12 de noviembre con la guía operativa y el recorrido de los tres retos. Python 3.12, Node 24 y google-adk 2.14.0.

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
| W10, W11 | Recorrido de los 17 pasos y lectura de los tres retos | Guía con preparación, carpetas, puertos, comandos, resultados y recuperación |
| Reto 1 | Agregar QA-05 en una instantánea de prueba | Cinco casos, 40 % inicial y 100 % corregido |
| Reto 2 | Ejecutar el revisor aislado con un modelo local inyectado | Sesión recibe evidencia real y diagnóstico inconsistente; salida estructurada identificada como prueba_local |

La versión anterior a integrar RAG tenía **16 pruebas aprobadas**. La versión integrada termina con **24 passed** al ejecutar `python -m pytest -q`. Las advertencias de SequentialAgent corresponden a la API de compatibilidad de la versión fijada y están documentadas en README.md.

## Experiencia 4 opcional, RAG (T9)

Validación de la integración del 12 de noviembre de 2026. `python -m pytest -q` termina con **24 passed**, con tres advertencias de deprecación de SequentialAgent.

| Criterio | Comprobación | Resultado |
|---|---|---|
| R1, R2 | Búsqueda de operaciones gratuitas cobradas y de una consulta ajena | DEF-101 primero y lista vacía |
| R3, R5, R8 | Modo evidencia sobre la versión defectuosa | QA-02 y QA-03 citan fuentes recuperadas y el veredicto sigue en 2/4, 50 % |
| R4 | Fuente inventada | Rechazada por validación |
| R6 | Cambio de documento de conocimiento | Identidad distinta; sin conocimiento la identidad original se conserva |
| R7 | Dashboard en navegador integrado | Fuentes desplegables con extracto en cada hallazgo |
| W12 | Presentación | Cuarta tarjeta Opcional, 20 minutos, 5 pasos con prompts, sin errores de JavaScript |
| ADK | Runtime con modelo local inyectado | Tres herramientas, `{contexto?}` en el revisor y citas en el reporte |

| R9 | Consultas sucesivas en herramientas del agente | Instantánea de conocimiento conservada, fuentes acumuladas sin duplicados y reinicio en la siguiente ejecución |
| R6 | Cambio exclusivo en conocimiento/ durante vigilancia | Nuevo reporte con trigger cambio, misma fuente, mismo contrato y mismos resultados |
| R10 | Revisión del workflow | conocimiento/** incluido en push.paths |
| W12, P8 | Recorrido en navegador de los cinco pasos opcionales | Spec, plan, construcción, verificación y reto accesibles; temporizador base en 180 minutos |

Pendiente: la llamada a Gemini con `buscar_contexto`. No se configuró una clave para este ensayo. El runtime ADK se comprobó con un modelo local inyectado.

La comprobación de vigilancia detectó una lectura concurrente del historial durante una escritura atómica en Windows. Se sincronizó read_history con el mismo bloqueo usado por persist_report y las 24 pruebas finalizaron correctamente.

## Preparación con un comando (T10)

Validación local del 12 de noviembre de 2026 con Windows PowerShell 5.1. La suite completa termina con **30 passed**, con las tres advertencias ya conocidas de SequentialAgent.

| Criterio | Comprobación | Resultado |
|---|---|---|
| E1, E2, E3 | Preparación completa en una copia dentro de una ruta con espacios | Kit inicial, venv nueva, dependencias instaladas, tres skills y 2/4 pruebas; clave vacía y ningún agente ni página resueltos |
| E4 | Repetir tras editar motor, skill, agente y .env | Archivos conservados y 4/4 pruebas de la versión corregida; pip reutiliza dependencias y comprueba las versiones requeridas |
| E5 | Reanudar una preparación interrumpida y recuperar un archivo ausente | Continúa sobre la venv y agrega lo ausente sin reemplazar el trabajo |
| E6 | Intentar reanudar una carpeta ajena | Rechazo y archivos anteriores conservados |
| E7 | Simular ausencia de Python y Node | Mensaje para TI, salida 1, sin crear la práctica ni instalar herramientas |
| E8 | Lanzar antes de construir el agente o pedir modo evidencia para el revisor | Mensaje del módulo pendiente o modo incompatible, sin ejecución inesperada |
| E8 | Ejecutar taller.ps1 flujo -Modo evidencia en una práctica preparada con agentes de referencia | Reporte real en modo evidencia, 4/4, sin activar el entorno manualmente y sin Gemini |
| E9, W13 | HTML en navegador integrado | Comando previo único, API key después de la construcción y reutilización del servidor en el bloque 3 |
| Compatibilidad | Parser de Windows PowerShell 5.1 | Scripts sin errores de sintaxis |

Los ensayos completos usan una copia temporal dentro de practica/, ignorada por Git, con las herramientas del sistema ya instaladas. Los registros locales quedan en salida/ensayo-preparacion*.log y no se publican. La preparación instala dependencias Python; la instalación de Python, Node, Antigravity y la autorización de políticas corporativas se deja a TI según lo solicitado. La clave y el acceso real a Gemini siguen pendientes de la configuración del facilitador y de cada equipo.

## Capturas

- capturas/dashboard-con-fallas.jpg muestra 2 aprobadas, 2 fallidas y 50 %.
- capturas/dashboard-corregido.jpg muestra 4 aprobadas, 0 fallidas y 100 %.
- capturas/presentacion-agente.jpg muestra la spec, instrucciones y prompt copiable de la primera experiencia.
- capturas/presentacion-autocontenida.jpg muestra las tres tarjetas después de integrar los recursos en el HTML.
- capturas/guia-recorrido-retos.jpg registra el último reto después de recorrer las tres experiencias.
- capturas/presentacion-rag-integrada.jpg muestra los tres módulos base y la cuarta experiencia opcional.
- capturas/dashboard-rag-integrado.jpg muestra el extracto recuperado de DEF-101 en el hallazgo QA-02.
- capturas/preparacion-un-comando.jpg muestra el comando único y los requisitos de preparación en el HTML.

## Validaciones pendientes

- Llamada a Gemini real. El usuario configurará la clave cuando revise la demo. El ensayo ADK utiliza un modelo local inyectado y no acredita una llamada a la API.
- Evaluación semántica del reto del revisor con Gemini. scripts/probar_revisor.py permite ejecutar el caso real tras configurar la clave. La prueba local del runtime acredita la integración y el contrato de estado.
- Ejecución remota en GitHub Actions. Se entregó el workflow para push y ejecución manual. Requiere subir el proyecto y configurar secretos y variables en GitHub.

El dashboard abre inicialmente la versión defectuosa para que la demostración tenga un antes y después. La ausencia de fallas de la versión corregida se refiere a los cuatro casos ejecutados.
