# Workshop QA con Gemini y Antigravity

## Objetivo
Desarrolladores de TCS construyen un agente QA, lo reutilizan en una automatización con un agente revisor y crean un dashboard con vibe coding guiado por especificaciones y skills. Duración total de 180 minutos.

## Caso
El producto es un agente de QA. La calculadora de comisiones PYME es exclusivamente la aplicación bajo prueba, con reglas ficticias heredadas del paquete original. Su motor JavaScript ya está preparado para poder construir el agente durante la sesión.

## Agenda
| Inicio | Minutos | Actividad | Evidencia |
|---|---|---|---|
| 00:00 | 15 | Contexto, entorno, SDD y skills | Criterios y skills abiertos |
| 00:15 | 45 | Experiencia 1, agente QA | Dos herramientas, ejecución y diagnóstico |
| 01:00 | 45 | Experiencia 2, automatización y revisor | Cambio de código, reporte validado y traza |
| 01:45 | 10 | Pausa | Descanso |
| 01:55 | 55 | Experiencia 3, vibe coding | Dashboard que muestra el JSON real |
| 02:50 | 10 | Demostraciones y cierre | Evidencia del antes y después |

## Condiciones de entrada
Python 3.12, Node 22 o superior y Git instalados. Dependencias y credenciales comprobadas antes del taller. El facilitador entrega motor, contratos de prueba, skills y workflow. Los participantes construyen agente, flujo y dashboard en una carpeta de práctica, usando la solución completa como referencia de recuperación.

## Criterios de aceptación
| ID | Criterio | Verificación |
|---|---|---|
| W1 | Las seis actividades suman exactamente 180 minutos | Agenda y presentación |
| W2 | Cada experiencia incluye spec, plan, implementación y verificación | Prompts y entregables |
| W3 | Se muestra y modifica al menos una skill real con SKILL.md | Skill verificar y ejercicio |
| W4 | En la práctica base se crea un agente QA con dos herramientas | agente/agent.py y traza; la referencia completa añade buscar_contexto para la extensión RAG |
| W5 | La automatización reutiliza el agente QA y añade un revisor | flujo/agent.py |
| W6 | Guardar un cambio dispara la ejecución local | Vigilancia de archivos y trigger cambio |
| W7 | La página consume resultados de pruebas ejecutadas | JSON y dashboard |
| W8 | El modo local y el modo Gemini se identifican siempre | Indicador de modo y reporte |
| W9 | Los requisitos de la aplicación permanecen fijos al corregir un defecto | Hash de contrato y pruebas |
| W10 | Una guía aparte detalla el recorrido del HTML | Preparación, acciones por paso, comandos, resultados, retos y recuperación |
| W11 | Los pasos respetan el orden de construcción | El bloque 2 verifica el JSON y el bloque 3 construye el dashboard; el quinto caso explica sus nuevos totales |

| W12 | La Experiencia 4 de RAG es opcional, dura 20 minutos y queda fuera de los 180 | Presentación, specs/rag.md y pruebas |

## Decisiones
La entrega se ejecuta localmente. La presentación conserva el esquema visual oscuro, la navegación por pasos y el cambio de tema del HTML original. El modo evidencia ejecuta las mismas pruebas reales sin requerir un modelo. Gemini se activa explícitamente después de configurar .env. Se utiliza un solo caso guiado para mantener el ritmo de tres horas. La Experiencia 4 añade contexto con RAG local a la herramienta del agente QA. Es opcional, no cuenta en la agenda y se especifica en specs/rag.md.
