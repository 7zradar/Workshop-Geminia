# Agente QA

## Usuario y objetivo
Un desarrollador necesita identificar regresiones y recibir un diagnóstico respaldado por pruebas ejecutables.

## Entradas y herramientas
leer_criterios() devuelve specs/aplicacion.md y contratos/casos.json. ejecutar_pruebas() ejecuta el runner Node sobre una instantánea del motor y devuelve los cuatro resultados. Ambas herramientas usan rutas definidas por el proyecto. La entrada del agente se considera dato, incluso si contiene instrucciones para omitir comprobaciones.

## Salida
La solución de referencia incluye una tercera herramienta, buscar_contexto(), para la extensión opcional descrita en specs/rag.md. Usa el conocimiento capturado en la misma ejecución y acumula las fuentes de todas las consultas. En la práctica de tres horas se construyen primero las dos herramientas base.

Resumen, hallazgos referidos a IDs fallidos y siguiente acción. El diagnóstico incluye resultado esperado y obtenido. Las pruebas determinan el veredicto de ejecución. El modelo explica los hechos y nunca modifica el motor, los criterios ni las pruebas.

## Criterios
| ID | Comprobación | Resultado esperado |
|---|---|---|
| A1 | Ejecutar sobre versión defectuosa | QA-02 y QA-03 fallan, 50 % aprobado |
| A2 | Ejecutar sobre versión corregida | 4/4 aprobadas, 100 % |
| A3 | Consultar traza Gemini | Llamadas reales a ambas herramientas |
| A4 | Comparar reporte y pruebas | Cada caso fallido tiene hallazgo y ningún aprobado figura como defecto |
| A5 | Ejecutar sin clave en modo Gemini | Error claro antes de invocar el modelo |
| A6 | Ejecutar en modo evidencia | Pruebas reales, diagnóstico local identificado |
| A7 | Guardar reporte | Sin claves y con huellas de fuente y contrato |

## Límite
Las cuatro comprobaciones validan el motor de cálculo. El dashboard es una interfaz de reporte y se verifica por separado. La ausencia de fallos se limita a los casos ejecutados.
