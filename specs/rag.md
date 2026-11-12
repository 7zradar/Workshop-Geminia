# Contexto con RAG (Experiencia 4, opcional)

## Usuario y objetivo
Un desarrollador quiere que cada hallazgo del agente QA cite la regla de negocio o el defecto anterior que lo respalda, sin que el modelo invente fuentes.

## Alcance
RAG significa recuperar, aumentar y generar. El agente recupera fragmentos de `conocimiento/` con una búsqueda local por palabras clave, los usa como contexto y cita su origen. No sustituye las pruebas: el veredicto lo siguen determinando los resultados de ejecución. La recuperación es determinista y no consume peticiones de Gemini. Los embeddings quedan como extensión.

## Entradas y salidas
`conocimiento/*.md` se divide en fragmentos por encabezado `##`. La fuente de cada fragmento es `archivo.md#Título`. La herramienta `buscar_contexto(consulta)` devuelve hasta tres fragmentos con fuente, título y extracto. Cada hallazgo añade `sources`, una lista de fuentes. El reporte añade `context`, los fragmentos recuperados en esa ejecución.

## Criterios
| ID | Comprobación | Resultado esperado |
|---|---|---|
| R1 | Buscar "operaciones gratuitas cobradas" | Devuelve DEF-101 y la regla de tarifa |
| R2 | Consulta sin relación con la base | Lista vacía, sin resultados forzados |
| R3 | Ejecutar QA en la versión defectuosa | QA-02 y QA-03 citan fuentes recuperadas en esa ejecución |
| R4 | Citar una fuente que no se recuperó | El reporte se rechaza y se conserva el último válido |
| R5 | Los hallazgos con fuentes | El veredicto y los conteos no cambian |
| R6 | Cambiar un documento de conocimiento | Nueva huella y un reporte distinto por contenido y modo |
| R7 | Dashboard | Muestra las fuentes de cada hallazgo y su extracto con textContent |
| R8 | Modo del reporte | Evidencia usa recuperación local; Gemini la usa como herramienta del agente |

## Límite
Los documentos son ficticios. Una cita demuestra que existe respaldo en la base, no que la recomendación sea correcta. Esa comprobación sigue en las pruebas y en el revisor.
