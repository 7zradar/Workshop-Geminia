# Convenciones del workshop QA

Lee specs/workshop.md y la spec del componente antes de modificarlo. Relaciona cada cambio con una tarea de specs/plan.md y ejecuta su comprobación. Las skills de Antigravity están en .agents/skills/.

Las expectativas de contratos/casos.json son la referencia de aceptación. Cuando la implementación incumpla un criterio claro, corrige la implementación. Modifica la spec cuando el requisito cambie o sea ambiguo y explica el cambio.

El agente QA y el revisor conservan los resultados originales. El veredicto lo determinan las pruebas. El modo evidencia está identificado y Gemini se activa con una clave local. Las claves pertenecen a .env o a secrets, y los datos de la demo son ficticios.

Usa rutas acotadas, argumentos de subprocess como listas y escrituras atómicas. Conserva un solo reporte por combinación de contenido y modo. Muestra errores de ejecución sin reemplazar el último reporte válido.
