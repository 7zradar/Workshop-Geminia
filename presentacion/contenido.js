/* Guion de tres horas. Cada paso contiene instrucciones utilizables y su evidencia. */
window.WORKSHOP_MODULES = [
  {
    id: 1,
    title_es: "Construye tu agente QA",
    title_en: "Build your QA agent",
    minutes: 45,
    description:
      "De una especificación a dos herramientas y un diagnóstico verificable.",
    steps: [
      {
        label: "Spec",
        minutes: 8,
        title: "Define qué debe comprobar el agente",
        body: "<p>El agente es de QA. Su aplicación bajo prueba es un motor de cálculo pequeño, con un bug preparado. Abre <code>specs/aplicacion.md</code> y <code>contratos/casos.json</code>. Con 20 operaciones y 4 transferencias, el criterio exige 74 y el motor inicial devuelve 99.</p><ol><li>Abre tu carpeta de práctica en Antigravity.</li><li>Invoca la skill <code>/especificar</code> y revisa los criterios antes de generar código.</li><li>Comprueba que cada hallazgo conserve el ID de la prueba y su evidencia.</li></ol>",
        prompt:
          "/especificar Crea specs/agente-qa.md. Construiremos un agente QA en Python con ADK. Lee specs/aplicacion.md y contratos/casos.json. Define dos herramientas, leer_criterios() y ejecutar_pruebas(), que usen qa_core.Evidence sobre una Snapshot. El agente debe ejecutar ambas, explicar esperado y obtenido y devolver summary, findings [{case_id, description, recommendation}] y next_action. Incluye criterios para la versión defectuosa (2 fallas, 50 %), corregida (0 fallas, 100 %) y trazabilidad. La spec debe distinguir modo evidencia de llamadas reales a Gemini. Espera la revisión del equipo antes de implementar.",
        done: "Spec revisada con entradas, dos herramientas, salida y criterios de aceptación.",
      },
      {
        label: "Skill",
        minutes: 4,
        title: "Haz explícita la forma de trabajar",
        body: "<p>Abre <code>.agents/skills/verificar/SKILL.md</code>. Identifica su <code>name</code>, <code>description</code> y procedimiento. Las skills guían a Antigravity durante la construcción. El agente QA que vas a crear ejecutará sus propias herramientas ADK.</p><ol><li>Agrega a la skill la obligación de incluir el ID y la evidencia de cada caso fallido.</li><li>Invócala por nombre en una petición.</li><li>Comprueba que el resultado siga ese formato.</li></ol>",
        prompt:
          "Revisa la skill verificar de este workspace. Añade una comprobación para que cada defecto incluya su ID, el criterio, el valor esperado y el valor obtenido. Aplica esta skill cuando verifiquemos el agente. Conserva las expectativas del contrato de pruebas.",
        done: "Una skill real editada y su aplicación identificada en la conversación.",
      },
      {
        label: "Plan",
        minutes: 5,
        title: "Revisa el plan antes de construir",
        body: "<p>Usa Planning o <code>/plan</code>. Revisa qué archivos propone tocar Antigravity y cómo verificará cada tarea. El kit ya proporciona el runner, la persistencia y el servidor.</p><ol><li>Separa herramientas, agente y verificación.</li><li>Comprueba que reutilice <code>qa_core.py</code>.</li><li>Comenta el plan y apruébalo cuando cubra los criterios.</li></ol>",
        prompt:
          '/plan Lee specs/agente-qa.md. Escribe specs/agente-plan.md con T1 herramientas, T2 agente y T3 verificación. Usa qa_core.Evidence y Snapshot, y exporta create_agent(evidence, model=None) y root_agent desde agente/agent.py. La herramienta ejecutar_pruebas debe guardar el resultado en tool_context.state["evidencia"]. El agente guarda el diagnóstico JSON en output_key "diagnostico". Incluye archivos y verificación por tarea. Espera la revisión antes de implementar.',
        done: "Plan revisado con tareas pequeñas y comprobaciones observables.",
      },
      {
        label: "Construir",
        minutes: 15,
        title: "Construye una tarea y observa su resultado",
        body: "<ol><li>Usa <code>/implementar</code> sobre T1. Revisa el diff.</li><li>Repite con T2 y T3.</li><li>El modelo se lee de <code>GEMINI_MODEL</code> y la clave de <code>.env</code>.</li><li>Abre <code>adk web</code> desde la raíz de la práctica y elige <code>agente</code>.</li></ol><p>Si tu equipo necesita recuperarse, compara con la solución completa que entregó el facilitador.</p>",
        prompt:
          "/implementar T1 de specs/agente-plan.md. Reutiliza Evidence del kit, con docstrings claros y argumentos tipados. Ejecuta su verificación y muestra el diff. Al terminar, detente para que el equipo revise. Repetiremos después con las tareas restantes.",
        command: "adk web",
        done: "Agente visible y herramientas conectadas al runner real.",
      },
      {
        label: "Verificar",
        minutes: 10,
        title: "Muestra la ejecución, no solo la respuesta",
        body: "<ol><li>Pide al agente revisar la versión actual.</li><li>En Events identifica <code>leer_criterios</code> y <code>ejecutar_pruebas</code>.</li><li>Comprueba QA-02 esperado 25, obtenido 50 y QA-03 esperado 74, obtenido 99.</li><li>Relaciona cada hallazgo con la tabla de la spec.</li></ol><p>La solución tiene modo evidencia para ensayar sin clave. El ensayo de los dos agentes usa <code>--mode gemini</code> después de configurar la clave.</p>",
        prompt:
          "/verificar specs/agente-qa.md. Comprueba las dos herramientas, la cobertura de los dos casos fallidos y que el agente conserve esperado y obtenido. Entrega la tabla criterio, evidencia y resultado. Indica si la prueba llamó a Gemini o se ejecutó localmente.",
        command: "python procesar.py --mode evidencia",
        done: "Dos defectos reproducibles y evidencia de cómo se obtuvieron.",
      },
      {
        label: "Reto",
        minutes: 3,
        title: "Un caso límite que el agente pueda explicar",
        body: "<p>Agrega una prueba para 11 operaciones y 0 transferencias. La especificación exige 27.50. El agente debe incorporar el resultado y conservar su ID.</p><p>Si la implementación falla, corrige el motor contra el criterio acordado. Una ambigüedad de requisitos se registra primero en la spec.</p>",
        prompt:
          "/especificar Añade QA-05 con 11 operaciones y 0 transferencias, esperado 27.50. Actualiza la spec antes de agregar el caso al contrato y repetir la verificación. Explica qué límite cubre.",
        done: "Un caso adicional que cubre el primer valor después del tramo gratuito.",
      },
    ],
  },
  {
    id: 2,
    title_es: "Automatiza y añade un revisor",
    title_en: "Automate and add a reviewer",
    minutes: 45,
    description:
      "El mismo agente se ejecuta con un disparador y un segundo agente revisa la evidencia.",
    steps: [
      {
        label: "Spec",
        minutes: 8,
        title: "Define el flujo y su segundo agente",
        body: "<p>Especifica un flujo <strong>cambio de código → agente QA → agente revisor → reporte JSON</strong>. El revisor recibe todos los resultados y comprueba que el diagnóstico corresponda a las fallas reales.</p><p>Los resultados de las pruebas determinan si el motor cumple. La revisión se refiere a la consistencia del reporte.</p>",
        prompt:
          "/especificar Crea specs/flujo.md. Reutiliza el agente QA anterior y añade un revisor ADK sin herramientas. Recibe diagnostico y evidencia en el estado, y devuelve decision VALIDADO u OBSERVADO y observations. Disparadores: cambio local en app/calculadora.mjs, ejecución manual y push en GitHub Actions. Registra una fila lógica por combinación de fuente, contrato y modo. Conserva el último reporte válido ante errores y muestra su origen. Incluye criterios de repetición y cambio automático.",
        done: "Spec con dos agentes, disparador, errores y contrato del reporte.",
      },
      {
        label: "Plan",
        minutes: 5,
        title: "Reutiliza el agente que ya construiste",
        body: "<p>El kit incluye <code>procesar.py</code> y <code>servidor.py</code>. Implementa <code>flujo/agent.py</code> usando las interfaces de esos archivos. Revisa que el segundo agente reciba la evidencia completa.</p>",
        prompt:
          '/plan Lee specs/flujo.md y procesar.py. Propón T1 modelos Analysis y Review con Pydantic, T2 create_pipeline(evidence, model) que conecta create_agent del módulo anterior y un revisor con SequentialAgent, T3 verificación del flujo. El QA usa output_key diagnostico y el revisor output_key revision. El revisor lee {diagnostico} y {evidencia}, usa output_schema Review e include_contents="none". Reutiliza la infraestructura del kit.',
        done: "El plan conecta ambos agentes mediante estado compartido.",
      },
      {
        label: "Construir",
        minutes: 15,
        title: "Añade una revisión verificable",
        body: "<ol><li>Implementa las tareas del flujo con <code>/implementar</code>.</li><li>Configura la clave en <code>.env</code>.</li><li>Ejecuta el flujo con Gemini.</li><li>Abre el reporte y localiza herramientas, diagnóstico y respuesta del revisor.</li></ol><p>La revisión debe cubrir todos los casos fallidos y señalar cualquier conclusión sin respaldo.</p>",
        prompt:
          "/implementar T1 de specs/flujo-plan.md. Define los modelos esperados por procesar.py y verifica su validación. Después implementaremos el pipeline y su comprobación. Conserva la evidencia de las herramientas y limita los hallazgos a los casos fallidos.",
        command: "python procesar.py --mode gemini",
        done: "Dos agentes ejecutados y un reporte estructurado con su traza.",
      },
      {
        label: "Automatizar",
        minutes: 10,
        title: "Guardar el código dispara una revisión",
        body: "<ol><li>Inicia el servidor y comprueba que la vigilancia está activa.</li><li>Abre el dashboard con el facilitador.</li><li>Corrige la operación cobrada con <code>Math.max(0, operaciones - 10)</code> y guarda el archivo.</li><li>Espera la ejecución con disparador <code>cambio</code>.</li></ol><p>En GitHub, agrega GOOGLE_API_KEY como secret y GEMINI_MODEL como variable. El workflow incluido sube el reporte como artefacto. Una ejecución con defectos termina en rojo y conserva el reporte.</p>",
        prompt:
          "Lee specs/flujo.md y revisa .github/workflows/qa.yml. Explica qué cambio lo dispara, dónde se configura la clave y cómo se conserva el artefacto cuando una prueba falla. Comprueba la vigilancia local guardando una corrección en app/calculadora.mjs.",
        command: "python servidor.py --mode gemini",
        done: "Cambio de código seguido de ejecución automática y reporte nuevo.",
      },
      {
        label: "Verificar",
        minutes: 5,
        title: "Compara antes y después",
        body: "<p>La versión inicial tiene 2/4 aprobadas. La corregida tiene 4/4. Comprueba que la huella del código cambió y la del contrato se conservó. Repite la misma versión y verifica que el historial conserve un único registro por contenido y modo.</p>",
        prompt:
          "/verificar specs/flujo.md. Comprueba el disparador cambio, el segundo agente, la correspondencia del reporte con las pruebas, la identidad por contenido y la conservación del último reporte ante errores. Muestra evidencia por criterio.",
        done: "Falla reproducida, corrección verificada y repetición sin duplicados.",
      },
      {
        label: "Reto",
        minutes: 2,
        title: "Pon a prueba al revisor",
        body: "<p>Propón un diagnóstico que afirme que todo pasó cuando existe una prueba fallida. El revisor debe marcarlo OBSERVADO y explicar qué ID contradice esa afirmación.</p><p>Después de este bloque corresponde una pausa de 10 minutos.</p>",
        prompt:
          "Comprueba el revisor con evidencia donde QA-03 falla y un diagnóstico que dice que todas las pruebas pasaron. Debe devolver OBSERVADO y mencionar la contradicción concreta.",
        done: "El revisor detecta un diagnóstico que contradice los resultados originales.",
      },
    ],
  },
  {
    id: 3,
    title_es: "Construye el dashboard con vibe coding",
    title_en: "Build the dashboard with vibe coding",
    minutes: 55,
    description:
      "De la spec de interfaz a una página que muestra el reporte real del agente.",
    steps: [
      {
        label: "Spec",
        minutes: 10,
        title: "Especifica lo que la página debe demostrar",
        body: "<p>El dashboard es el producto visible de la revisión. Abre <code>salida/ultimo.json</code> y usa ese contrato real. Debe mostrar totales, porcentaje, hallazgos, revisión y evidencia de cada caso.</p><p>Escribe primero los criterios. Con cuatro pruebas y dos fallas debe mostrar 50 %. Al cargar la versión corregida, 100 %.</p>",
        prompt:
          "/especificar Crea specs/pagina.md para un dashboard QA con HTML, CSS y JavaScript. Usa el contrato real de salida/ultimo.json. Incluye total, aprobadas, fallidas, porcentaje, lista filtrable de casos con esperado y obtenido, diagnóstico, revisión y traza. Permite importar JSON y conserva los datos ante un archivo inválido. Distingue modo evidencia y Gemini. Responsive desde 375 px y usable con teclado. Los controles locales usan las rutas existentes de servidor.py. No expongas claves en la página.",
        done: "Spec de interfaz con datos reales y casos comprobables.",
      },
      {
        label: "Plan",
        minutes: 8,
        title: "Define una construcción que puedas revisar",
        body: "<p>Revisa la skill <code>implementar</code> y el plan de la página. Empieza por validar el JSON y calcular el resumen, continúa con la tabla y termina con controles y accesibilidad.</p>",
        prompt:
          "/plan Lee specs/pagina.md y servidor.py. Escribe specs/pagina-plan.md. Divide el trabajo en validación y renderizado de JSON, interfaz y filtros, integración local y verificación visual. Reutiliza las rutas /api/report, /api/status, /api/run y /api/history. Renderiza textos importados con textContent. Incluye el comportamiento cuando el servidor no está disponible.",
        done: "Plan con archivos, contrato de datos y comprobaciones por tarea.",
      },
      {
        label: "Construir",
        minutes: 20,
        title: "Deja que Antigravity escriba y revisa el diff",
        body: "<ol><li>Implementa cada tarea con la skill correspondiente.</li><li>Prueba primero un reporte guardado de la versión defectuosa.</li><li>Conecta la página al servidor y ejecuta QA.</li><li>Solicita los cambios de alcance actualizando la spec.</li></ol><p>Al abrir directamente el HTML se muestra un ejemplo guardado y se puede importar JSON. La automatización se usa con el servidor iniciado.</p>",
        prompt:
          "/implementar T1 de specs/pagina-plan.md. Usa HTML, CSS y JavaScript sin frameworks. Valida el contrato antes de reemplazar los datos visibles. Haz que el filtro conserve los contadores globales y muestra siempre el origen de la ejecución. Revisa el diff antes de avanzar a las siguientes tareas.",
        command: "python servidor.py",
        done: "Dashboard que carga y presenta el reporte de QA.",
      },
      {
        label: "Verificar",
        minutes: 12,
        title: "Comprueba la página contra la spec",
        body: "<ol><li>En el navegador comprueba 4 pruebas, 2 fallas y 50 %.</li><li>Filtra fallidos y abre esperado y obtenido.</li><li>Aplica la corrección y espera el nuevo reporte automático.</li><li>Importa un JSON inválido y conserva el último resultado visible.</li><li>Recorre los controles con Tab y verifica el ancho de 375 px.</li></ol>",
        prompt:
          "/verificar specs/pagina.md. Comprueba en el navegador los reportes defectuoso y corregido, el filtro, importación inválida, teclado y ancho móvil. Toma capturas y entrega un walkthrough que vincule criterio y evidencia. Registra las validaciones pendientes, incluidas las que requieren Gemini real.",
        done: "Walkthrough con resultados, capturas y criterios cumplidos.",
      },
      {
        label: "Reto",
        minutes: 5,
        title: "Cuenta la historia con evidencia",
        body: "<p>Agrega una mejora definida en la spec, como filtrar casos por ID o comparar dos ejecuciones. Prepara una demo de dos minutos.</p><ol><li>Muestra la spec y una skill aplicada.</li><li>Abre un hallazgo y su evidencia.</li><li>Muestra la automatización y el segundo agente.</li><li>Termina con el dashboard después de corregir el bug.</li></ol>",
        prompt:
          "/especificar Añade un filtro por ID de caso al dashboard. Define su criterio, actualiza el plan, implementa el cambio y verifica que los totales globales se conserven.",
        done: "Entrega con tres specs, skills usadas, dos agentes, automatización y página.",
      },
    ],
  },
];
for (const module of window.WORKSHOP_MODULES) {
  module.steps_es = module.steps.map((step) => step.label);
  module.steps_en = module.steps_es;
}
