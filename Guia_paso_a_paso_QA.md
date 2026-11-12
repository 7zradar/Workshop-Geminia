# Guía paso a paso del workshop QA

Esta guía acompaña a WORKSHOP_GEMINI.html y desarrolla sus tres experiencias. Está pensada para quien facilita el taller y para los equipos que construyen los entregables. La sesión dura tres horas y la preparación del entorno se completa previamente.

El HTML marca el recorrido y contiene los prompts. Durante cada paso abres Antigravity, revisas o generas archivos, ejecutas la comprobación y contrastas el resultado con la spec. Avanzas cuando puedes mostrar la evidencia indicada en «Listo cuando».

## 1. Entiende las piezas antes de comenzar

| Pieza | Qué significa en este taller | Dónde la ves |
|---|---|---|
| Aplicación bajo prueba | Calculadora ficticia que contiene un error intencional | app/calculadora.mjs |
| Spec del producto | Reglas y resultados esperados que debe cumplir la calculadora | specs/aplicacion.md y contratos/casos.json |
| Antigravity | Herramienta con la que el equipo genera y revisa código | Panel del agente y editor |
| Skills | Procedimientos reutilizables para especificar, implementar y verificar | .agents/skills/ |
| Agente QA | Programa que consulta criterios, ejecuta herramientas y explica las fallas | agente/agent.py |
| Agente revisor | Programa que contrasta el diagnóstico con la evidencia original | flujo/agent.py |
| Automatización | Disparador que ejecuta el flujo cuando cambia el código | servidor.py o GitHub Actions |
| Dashboard | Página que muestra el reporte generado | pagina/index.html |

El mismo agente QA del primer bloque participa en el flujo del segundo. En el tercero construyes una página para ver sus resultados.

## 2. Preparación previa con un solo comando

### 2.1 Descarga y requisitos que comprueba TI

Descarga el [ZIP del repositorio completo](https://github.com/7zradar/Workshop-Geminia/archive/refs/heads/codex/qa-workshop.zip) y extráelo. Para construir los entregables no basta con descargar solo el HTML. Si ya tienes la rama codex/qa-workshop, utiliza tu copia actualizada.

Antes del evento necesitas Antigravity con sesión iniciada, Python 3.12 y Node 22 o superior. El preparador no instala herramientas del sistema: si falta Python o Node indica qué debe instalar TI. Con el ZIP no necesitas instalar Git. También necesitas conexión para instalar las dependencias Python.

### 2.2 Ejecuta una sola preparación

Abre PowerShell en la carpeta que contiene preparar-workshop.ps1 y ejecuta:

```powershell
powershell -NoProfile -File .\preparar-workshop.ps1
```

Este comando comprueba Python y Node, crea practica/equipo-01, prepara su entorno .venv, instala las dependencias y verifica las tres skills y las pruebas locales. No necesitas ejecutar pip, crear ni activar .venv manualmente. No solicita la API key ni llama a Gemini. Los agentes y la página quedan por construir.

Espera **PREPARACION COMPLETA**. En el kit nuevo se esperan cuatro pruebas, dos aprobadas y dos fallidas: 50 %. Las fallas intencionales acreditan que el runner funciona. El informe está en practica/equipo-01/salida/preparacion.json.

Si la preparación se interrumpe, resuelve el mensaje y repite el mismo comando. Reutiliza las dependencias preparadas y completa solo archivos ausentes de un kit identificado; conserva código, contratos, skills y .env existentes. Si esa carpeta contiene trabajo previo sin la marca del preparador, elige otro nombre, por ejemplo agregando `-Equipo equipo-02` al mismo comando. No sobrescribe una carpeta ajena.

Si la política corporativa bloquea scripts o descargas, comparte el mensaje con TI antes del taller. El preparador no cambia la política de ejecución, no instala Python ni Node y no modifica credenciales.

### 2.3 Abre la práctica en Antigravity

Abre la carpeta exacta indicada al finalizar: practica/equipo-01. Comprueba que puedes leer specs/aplicacion.md, contratos/casos.json y las tres skills. La infraestructura ya está lista. Construirás agente/agent.py, flujo/agent.py y pagina/index.html con los prompts del HTML.

**La API key se configura después de construir el primer agente, antes de ejecutarlo con Gemini.** En ese momento abre el .env de esta práctica y completa GOOGLE_API_KEY una sola vez. El agente QA, el revisor y RAG reutilizan esa configuración. No necesitas una clave diferente por agente ni volver a introducirla en cada bloque.

Los comandos cortos taller.ps1 usan directamente el entorno de la práctica. Antigravity puede ejecutarlos en su terminal. No necesitas activar .venv en cada terminal.

| Momento | Acción en la carpeta de práctica |
|---|---|
| Agente construido y clave configurada | `.\taller.ps1 agente` abre ADK Web en http://127.0.0.1:8000 |
| Flujo construido | `.\taller.ps1 flujo` ejecuta QA y revisor una vez |
| Automatización | `.\taller.ps1 automatizar` inicia la vigilancia en el puerto 8767 |
| Reto del revisor | `.\taller.ps1 revisor` ejecuta el diagnóstico inconsistente |
| Dashboard construido | Abrir http://127.0.0.1:8767/ usando el servidor ya iniciado |

### 2.4 Referencia del facilitador

La raíz del repositorio contiene la solución completa. Para ensayar esa referencia, usa `.\iniciar.ps1`: prepara su entorno y abre el servidor en el puerto 8765, en modo evidencia. La presentación está en http://127.0.0.1:8765/presentacion. El HTML también abre por sí solo con doble clic.

La referencia y la práctica son proyectos separados. La preparación no copia la clave de la referencia a los participantes. Como facilitador, ensaya una llamada real antes del evento usando tu propia configuración. Las comprobaciones adicionales de pytest y las alternativas de comandos pertenecen a la validación del facilitador y no a la preparación manual del participante.

### 2.5 Carpetas y terminales durante el taller

| Lugar | Uso | Puerto |
|---|---|---|
| Raíz de la solución completa | Referencia y demostración del facilitador | 8765 |
| practica/equipo-01 | Workspace que abre el participante en Antigravity | Sin servidor propio hasta ejecutarlo |
| Terminal A de la práctica | ADK Web durante el primer bloque | 8000 |
| Terminal A tras detener ADK Web con Ctrl+C | Vigilancia del bloque 2 y dashboard del bloque 3 | 8767 |
| Terminal B de la práctica | Ejecución puntual del flujo y reto del revisor | Sin servidor propio |

El servidor se inicia una vez en el bloque 2 y sigue funcionando mientras construyes el dashboard. Las direcciones 127.0.0.1 apuntan al equipo donde se abre el navegador. Cada participante ejecuta su práctica en su computadora. Specs, skills y vibe coding se aplican desde el primer módulo.

## 3. Cómo llevar el ritmo de las tres horas

| Hora transcurrida | Actividad |
|---|---|
| 00:00–00:15 | Apertura y comprobación del entorno |
| 00:15–01:00 | Experiencia 1, agente QA |
| 01:00–01:45 | Experiencia 2, automatización y revisor |
| 01:45–01:55 | Pausa |
| 01:55–02:50 | Experiencia 3, dashboard con vibe coding |
| 02:50–03:00 | Demostraciones y cierre |

En cada paso explica el resultado buscado, muestra un ejemplo breve y deja que los equipos lo hagan. La explicación y la práctica comparten el tiempo indicado. El HTML tiene un temporizador que puedes iniciar y pausar.

## 4. Apertura de quince minutos

1. Abre WORKSHOP_GEMINI.html y despliega «Apertura · 15 min · entorno, specs y skills».
2. Explica el objetivo con una frase. «Vamos a construir un agente QA que encuentre una diferencia, la documente y vuelva a revisar el código después de corregirla».
3. Abre specs/aplicacion.md y lee la regla de las primeras diez operaciones gratuitas.
4. Haz el cálculo con el grupo. Para 20 operaciones y 4 transferencias corresponde 25 + 10 × 2.50 + 4 × 6 = 74.
5. Ejecuta el runner o muestra el resultado inicial del facilitador. El motor devuelve 99 en ese caso.
6. Presenta el ciclo spec, plan, tareas, implementación y verificación.
7. Pide que cada equipo tenga abierta su carpeta de práctica en Antigravity.

Pulsa «Comenzar las experiencias» y elige la primera tarjeta. En las siguientes secciones los nombres de cada paso coinciden con el HTML.

## 5. Experiencia 1, construye el agente QA

### 5.1 Spec, ocho minutos

**En el HTML** abre «Define qué debe comprobar el agente» y pulsa Copiar.

**En Antigravity** pega el prompt en el panel del agente. Antigravity debe leer specs/aplicacion.md y contratos/casos.json y escribir specs/agente-qa.md.

Abre el archivo generado y revisa con el equipo estas decisiones.

- El usuario es un desarrollador que necesita comprobar el motor.
- leer_criterios obtiene la spec y los casos del contrato.
- ejecutar_pruebas usa el runner del kit y devuelve resultados por caso.
- La salida incluye summary, findings y next_action.
- Cada hallazgo identifica un caso realmente fallido y sus valores esperado y obtenido.

Comprueba la tabla base antes de aprobar la spec.

| Caso | Entrada | Esperado | Obtenido con el bug |
|---|---|---|---|
| QA-01 | 0 operaciones, 0 transferencias | 25 | 25 |
| QA-02 | 10 operaciones, 0 transferencias | 25 | 50 |
| QA-03 | 20 operaciones, 4 transferencias | 74 | 99 |
| QA-04 | -1 operaciones, 0 transferencias | ERROR_VALIDACION | ERROR_VALIDACION |

**Avanza cuando** la spec describe las dos herramientas y los resultados son comprobables. Si Antigravity propone corregir el motor en este paso, acota la tarea a construir el agente que lo revisa.

### 5.2 Skill, cuatro minutos

**En el HTML** abre «Haz explícita la forma de trabajar».

Abre .agents/skills/verificar/SKILL.md en el editor. Muestra el name, la description y el procedimiento. Pide al equipo agregar una comprobación para que la evidencia identifique source_hash y contract_hash, además de los datos de cada falla.

Usa el prompt del HTML para realizar ese cambio. Revisa el diff de la skill. En una petición posterior menciona verificar y comprueba que Antigravity aplique esa comprobación.

Si la skill no aparece en el menú de comandos, escribe «Lee y aplica .agents/skills/verificar/SKILL.md a esta tarea». Esto permite comprobar su procedimiento durante la práctica.

**Avanza cuando** puedes explicar qué instrucción se agregó y cómo influye en la verificación.

### 5.3 Plan, cinco minutos

**En el HTML** abre «Revisa el plan antes de construir» y copia el prompt.

Usa Planning o /plan si está disponible. Antigravity debe escribir specs/agente-plan.md con tareas para herramientas, agente y verificación.

Antes de pulsar Proceed, comprueba que el plan reutiliza qa_core.py y contempla la interfaz que usará el segundo bloque.

| Elemento | Contrato que revisas |
|---|---|
| Función de construcción | create_agent(evidence, model=None) |
| Agente importable | root_agent |
| Salida del agente | output_key igual a diagnostico |
| Evidencia compartida | tool_context.state["evidencia"] |
| Herramientas | leer_criterios y ejecutar_pruebas |

**Avanza cuando** cada tarea tiene archivos y una forma de verificar el resultado.

### 5.4 Construir, quince minutos

**En el HTML** abre «Construye una tarea y observa su resultado».

1. Pega el prompt /implementar para T1.
2. Revisa el diff y el resultado de la comprobación.
3. Solicita T2 y luego T3 por separado.
4. Comprueba que existe agente/agent.py y que el modelo se obtiene de GEMINI_MODEL.
5. Pide a Antigravity comprobar localmente las herramientas. En este paso todavía no hace falta la API key.

**Avanza cuando** agente/agent.py está implementado y sus herramientas ejecutan las comprobaciones locales. La primera llamada a Gemini corresponde al siguiente paso.

### 5.5 Verificar, diez minutos

**En el HTML** abre «Muestra la ejecución, no solo la respuesta».

El agente ya está construido. Abre el .env de la práctica y configura GOOGLE_API_KEY una sola vez. Revisa GEMINI_MODEL si necesitas elegir otro modelo disponible. Después inicia la interfaz en la terminal A de la práctica:

```powershell
.\taller.ps1 agente
```

Abre http://127.0.0.1:8000, elige agente y pide revisar el motor actual contra la especificación, consultando criterios y ejecutando las pruebas. Conserva esa terminal abierta durante la comprobación.

1. En ADK Web abre Events y localiza leer_criterios y ejecutar_pruebas.
2. Abre la respuesta de la herramienta y revisa QA-02 y QA-03.
3. Contrasta el diagnóstico con esa evidencia.
4. Pega el prompt /verificar del HTML en Antigravity.
5. Guarda el walkthrough o las capturas que relacionan criterio y resultado.

Puedes ejecutar la misma comprobación del motor desde la terminal B.

```powershell
node scripts/ejecutar-pruebas.mjs
```

Ese comando comprueba las pruebas sin usar un modelo. En ADK Web verificas además las decisiones y las llamadas del agente.

**Entrega del bloque** con spec, plan, skill editada, agente y evidencia de sus dos herramientas.

### 5.6 Reto 1, tres minutos

El reto de extensión agrega QA-05 para comprobar el primer valor fuera del tramo gratuito.

1. Copia el prompt del paso «Un caso límite que el agente pueda explicar».
2. Revisa specs/aplicacion.md y los criterios de specs/agente-qa.md. Ambos deben reflejar el quinto caso y los nuevos totales antes de modificar el contrato.
3. Pide agregar este objeto al arreglo de contratos/casos.json, respetando sus comas.

```json
{
  "id": "QA-05",
  "name": "Primera operación adicional",
  "criterion": "25 + (11 - 10) × 2.50 = 27.50",
  "input": {"operaciones": 11, "interbancarias": 0},
  "expected": 27.50
}
```

4. Ejecuta el runner y solicita otra revisión al agente.

Con el bug, QA-05 obtiene 52.50 y falla. El total pasa a cinco casos, dos aprobados y tres fallidos, con 40 %. Después de corregirlo tendrás cinco aprobados y 100 %.

El facilitador puede mantener los cuatro casos base durante la sesión y dejar esta extensión para equipos que avancen rápido. Si un equipo la implementa, debe usar los nuevos totales en los siguientes bloques y guardar una nueva evidencia inicial.

## 6. Experiencia 2, automatiza y añade un revisor

### 6.1 Spec, ocho minutos

**En el HTML** abre «Define el flujo y su segundo agente».

Copia el prompt /especificar y revisa specs/flujo.md. La secuencia debe quedar definida como cambio de código, agente QA, agente revisor y reporte JSON.

Comprueba estas condiciones con el equipo.

- El agente QA se reutiliza desde el bloque anterior.
- El revisor recibe diagnostico y evidencia completos.
- decision acepta VALIDADO u OBSERVADO y observations explica sus motivos.
- Una nueva versión genera un reporte identificado por su contenido.
- Un error queda visible y se conserva el último reporte válido.

**Avanza cuando** el equipo puede explicar qué revisa el segundo agente y qué dispara el flujo.

### 6.2 Plan, cinco minutos

**En el HTML** abre «Reutiliza el agente que ya construiste».

Pega el prompt de planificación. Revisa que las tareas escriban specs/flujo-plan.md y flujo/agent.py, y que respeten las interfaces que consume procesar.py.

| Modelo o función | Campos o función esperados |
|---|---|
| Finding | case_id, description, recommendation |
| Analysis | summary, findings, next_action |
| Review | decision, observations |
| create_pipeline(evidence, model) | Conecta el QA anterior y el revisor |
| Estado de salida | diagnostico y revision |

**Avanza cuando** el plan muestra cómo llega la evidencia del primer agente al segundo.

### 6.3 Construir, quince minutos

**En el HTML** abre «Añade una revisión verificable».

1. Implementa las tareas de specs/flujo-plan.md con la skill implementar.
2. Revisa cada diff y comprueba los modelos de salida.
3. Detén ADK Web con Ctrl+C si vas a reutilizar su terminal.
4. En la carpeta de práctica ejecuta el flujo.

```powershell
.\taller.ps1 flujo
```

Abre salida/ultimo.json con Antigravity y localiza mode, summary, review y trace. Reutiliza el .env del bloque 1.

Con el contrato base y el motor defectuoso, el reporte tiene total 4, passed 2, failed 2 y percentage 50. Debes ver los actores agente_qa y revisor_qa en la traza de una ejecución Gemini.

VALIDADO significa que el diagnóstico es consistente con la evidencia. Puede aparecer junto con CON_FALLAS cuando el reporte describe correctamente los defectos.

Para ensayar los resultados y la persistencia local puedes ejecutar el modo evidencia. Su revisión local aparece identificada en el JSON.

```powershell
.\taller.ps1 flujo -Modo evidencia
```

**Avanza cuando** el flujo genera el JSON y la revisión cumple su esquema.

### 6.4 Automatizar, diez minutos

**En el HTML** abre «Guardar el código dispara una revisión».

En la terminal A de la práctica inicia el servidor. La vigilancia está activa por defecto.

```powershell
.\taller.ps1 automatizar
```

Abre http://127.0.0.1:8767/api/status en el navegador para comprobar su estado.

El campo watch debe ser True. Cuando la ejecución inicial termine, running pasa a False y error debe estar vacío. En este bloque puedes revisar el JSON directamente. El dashboard del equipo se construirá en la siguiente experiencia.

1. Conserva el reporte inicial generado dentro de salida/reportes/.
2. Abre app/calculadora.mjs.
3. Pide a Antigravity corregir el defecto de operaciones gratuitas contra la spec.
4. Revisa que operacionesCobradas quede definido con Math.max(0, operaciones - 10).
5. Guarda el archivo y espera que finalice la nueva revisión.

Abre salida/ultimo.json con Antigravity y revisa trigger, summary y review. También puedes abrir http://127.0.0.1:8767/api/report en el navegador.

Debes obtener trigger igual a cambio y 100 % de aprobación. Durante la ejecución Gemini pueden transcurrir varios segundos. Comprueba /api/status antes de concluir que el flujo falló.

El facilitador puede mostrar su dashboard de referencia en el puerto 8765 mientras los equipos revisan sus propios JSON en el 8767.

### 6.5 Verificar, cinco minutos

**En el HTML** abre «Compara antes y después».

1. Compara el reporte inicial y el corregido.
2. source_hash debe ser distinto y contract_hash debe coincidir si ambas ejecuciones usaron los mismos casos.
3. Consulta /api/history y localiza los reportes por ID.
4. En la terminal B repite la misma ejecución con el mismo modo.

```powershell
.\taller.ps1 flujo
```

El archivo y el registro del mismo ID se actualizan. El historial conserva un registro por combinación de contenido y modo. Las ejecuciones en modo evidencia y Gemini tienen identidades diferentes.

Pega el prompt /verificar del HTML y conserva la tabla de criterios con su evidencia.

**Entrega del bloque** con spec, plan, dos agentes, disparador automático y reportes antes y después.

### 6.6 Reto 2, dos minutos

Este reto aísla al segundo agente para comprobar si observa un diagnóstico que contradice las pruebas. El kit incluye un comando preparado.

```powershell
.\taller.ps1 revisor
```

El comando ejecuta pruebas reales sobre demo/version-con-error.mjs. Presenta al revisor un diagnóstico que afirma que todas pasaron y contiene findings vacío. Utiliza el mismo revisor de create_pipeline, con una sesión independiente.

Abre salida/reto-revisor.json y comprueba lo siguiente.

- evidence_summary conserva las fallas reales.
- failed_case_ids incluye los IDs que contradicen el diagnóstico.
- review.decision debe ser OBSERVADO.
- review.observations debe explicar la contradicción.
- passed es True cuando la decisión coincide con lo esperado.

El exit code es 0 cuando el revisor observa el caso, 1 cuando la decisión difiere y 2 ante un error de ejecución. El ensayo con Gemini real requiere la clave y el flujo ya implementado. El facilitador debe probar este comando antes del evento para usar los dos minutos en explicar el resultado.

## 7. Pausa de diez minutos

Conserva el servidor de la práctica activo para utilizarlo en el bloque siguiente. Guarda los reportes y los archivos del equipo antes de la pausa.

## 8. Experiencia 3, construye el dashboard con vibe coding

### 8.1 Spec, diez minutos

**En el HTML** abre «Especifica lo que la página debe demostrar».

Abre salida/ultimo.json y muestra sus campos. Copia el prompt /especificar para que Antigravity genere specs/pagina.md usando ese contrato real.

Revisa que la página incluya estos resultados observables.

- Total de pruebas, aprobadas, fallidas y porcentaje.
- Lista filtrable con ID, criterio, esperado y obtenido.
- Diagnóstico, revisión y traza.
- Indicación del modo de ejecución.
- Importación de un JSON y error visible ante un archivo inválido.
- Actualización al generarse otro reporte y controles utilizables con teclado.

Para una entrega base, cuatro casos con dos fallas deben mostrar 50 %. Si agregaste QA-05, usa cinco casos y tres fallas, con 40 %.

**Avanza cuando** cada función visible tiene un criterio verificable.

### 8.2 Plan, ocho minutos

**En el HTML** abre «Define una construcción que puedas revisar».

Pega el prompt de planificación y revisa specs/pagina-plan.md. Empieza por validación de datos, sigue con contadores y casos, y termina con integración y accesibilidad.

| Ruta existente | Uso para la página |
|---|---|
| GET /api/report | Reporte más reciente |
| GET /api/status | Ejecución, error, modo y vigilancia |
| GET /api/history | Reportes anteriores |
| GET /api/report/ID | Un reporte del historial |
| POST /api/run | Solicitar ejecución con el modo elegido |
| POST /api/watch | Activar o pausar vigilancia |
| POST /api/scenario | Aplicar una versión pedagógica del motor |

Las rutas están implementadas en servidor.py. En los controles POST revisa el objeto JSON que acepta cada ruta antes de generarlos. Los datos importados se presentan como texto mediante textContent.

**Avanza cuando** el plan utiliza el servidor y el contrato que ya tienes.

### 8.3 Construir, veinte minutos

**En el HTML** abre «Deja que Antigravity escriba y revisa el diff».

1. Implementa T1 de specs/pagina-plan.md con la skill implementar.
2. Verifica que un reporte válido se lea y que un archivo inválido produzca un error manejado.
3. Continúa con los contadores y la tabla de casos.
4. Añade el filtro y las secciones de diagnóstico y revisión.
5. Integra /api/report y la actualización de resultados.
6. Abre la página de tu equipo en [puerto 8767](http://127.0.0.1:8767/).

El servidor del segundo bloque puede seguir activo mientras guardas HTML, CSS y JavaScript. Si lo detuviste, reinícialo desde la raíz de la práctica con el comando del bloque anterior.

Usa un reporte inicial guardado en salida/reportes/ para comprobar las fallas. En la interfaz del facilitador puedes importar ese JSON o seleccionarlo desde el historial.

**Avanza cuando** los datos visibles coinciden con un reporte ejecutado.

### 8.4 Verificar, doce minutos

**En el HTML** abre «Comprueba la página contra la spec».

Haz esta secuencia con el equipo.

1. Carga el reporte inicial y verifica los contadores.
2. Filtra fallidos. Deben verse los casos fallidos y conservarse los totales globales.
3. Abre QA-03 y comprueba esperado 74 y obtenido 99.
4. Consulta diagnóstico, revisión y traza. Comprueba el modo.
5. Vuelve a la vista de ejecución actual antes de probar una actualización automática si estabas consultando un reporte importado o del historial.
6. Repite el cambio del motor y espera el reporte de la versión corregida.
7. Comprueba 100 % y que no se presentan defectos sobre casos aprobados.
8. Importa un JSON inválido y verifica que el mensaje de error conserve el reporte anterior.
9. Usa Tab y Enter para recorrer los controles y prueba un ancho de 375 px.
10. Usa /verificar y conserva un walkthrough por criterio.

Para volver al inicio del ejercicio puedes copiar la versión pedagógica con error al motor y guardar el cambio. Esta acción reemplaza el motor de la práctica por la referencia del ejercicio.

```powershell
Copy-Item -LiteralPath .\demo\version-con-error.mjs -Destination .\app\calculadora.mjs
```

Después corrígelo con Antigravity o usa el control Aplicar corrección si tu equipo implementó ese control. La solución completa del facilitador incluye ambos botones.

**Entrega del bloque** con página, spec, plan y evidencia de sus criterios.

### 8.5 Reto 3, cinco minutos

En el paso «Cuenta la historia con evidencia», añade un filtro por ID de caso.

1. Copia el prompt /especificar del HTML y define el nuevo criterio.
2. Actualiza el plan.
3. Implementa el filtro.
4. Busca QA-03 y comprueba que aparece el caso correspondiente.
5. Borra el filtro y recupera la lista completa.
6. Confirma que los contadores globales se conservan.

Usa el tiempo restante para preparar una demostración de dos minutos con la spec, la skill aplicada, el hallazgo, la automatización y el resultado corregido.

## 9. Cierre de diez minutos

Elige el número de equipos que alcance a presentar. Cada demostración muestra estos elementos.

| Tiempo de demo | Qué muestra el equipo |
|---|---|
| 0:00–0:20 | Spec y criterio de aceptación |
| 0:20–0:40 | Skill aplicada y herramientas del agente QA |
| 0:40–1:10 | Defecto con esperado y obtenido |
| 1:10–1:40 | Cambio de código, nueva ejecución y revisor |
| 1:40–2:00 | Dashboard y resultado final |

Cierra preguntando qué evidencia permitió aceptar el cambio y qué tarea cambió en su forma de trabajar con el agente.

## 10. Si un equipo se atasca

| Qué observa | Qué revisar o ejecutar |
|---|---|
| Solo ve código en GitHub | Descargar WORKSHOP_GEMINI.html con Download raw file y abrirlo en el navegador |
| No aparece una skill | Workspace correcto y archivo SKILL.md. Mencionar su ruta explícitamente |
| Python no encuentra google.adk | Entorno activo en esa terminal e instalación de requirements.txt |
| ADK Web no muestra agente | Carpeta agente y archivo agent.py creados, root_agent exportado y terminal en la raíz de la práctica |
| Gemini falla | .env de la práctica, clave, nombre de modelo, cuota y conexión |
| Node termina con código 1 | Revisar JSON. Dos fallas intencionales son el resultado inicial esperado |
| Tiene 40 % en vez de 50 % | Verificar si añadió QA-05 y tiene cinco casos |
| /api/status muestra error | Leer el mensaje y conservar el último reporte válido mientras se corrige la causa |
| No ve página en el bloque 2 | Revisar salida/ultimo.json o /api/report. La página se construye en el bloque 3 |
| No cambia el reporte al guardar | Carpeta y puerto correctos, watch activo y contenido del motor realmente cambiado |
| Dashboard conserva un reporte antiguo | Revisar si está en un reporte importado o histórico y volver a ejecutar QA |
| Puerto ocupado | Reutilizar la terminal del servidor existente o elegir otro --port |
| Se retrasa al generar código | Comparar ese componente con la solución del facilitador y volver a su criterio |

## 11. Extensión opcional de GitHub Actions

El disparador local permite cumplir el bloque de automatización dentro de la sesión. El workflow incluido permite repetirlo desde GitHub cuando el equipo tenga listo su repositorio.

1. Sube el trabajo a una rama del repositorio del equipo.
2. En Settings, Secrets and variables, Actions, configura GOOGLE_API_KEY como secret y GEMINI_MODEL como variable.
3. En Actions elige QA con Gemini y Run workflow.
4. Selecciona la rama del equipo y el modo gemini o evidencia.
5. Abre el resultado del job y descarga el artefacto reporte-qa.
6. Importa el JSON del artefacto en el dashboard.

workflow_dispatch necesita que la definición del workflow esté también en la rama por defecto para habilitar su uso manual. El disparador push funciona según los paths definidos en el archivo. Una ejecución con los defectos intencionales puede terminar en rojo y conservar el artefacto, tal como define --fail-on-defects. [Documentación de ejecución manual de GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

## 12. Qué se comprobó al preparar esta guía

Se recorrieron las tres experiencias del HTML. Se aclaró el uso de JSON en el segundo bloque, los puertos de práctica y los totales del quinto caso. La infraestructura dispone de una comprobación local de cinco casos y una prueba del runtime del revisor aislado con un modelo de prueba identificado.

La llamada a Gemini real y la evaluación semántica del reto del revisor quedan pendientes de la clave y el ensayo previo del facilitador. El recorrido de las diapositivas y las pruebas locales permiten preparar esos pasos con evidencia explícita.

## 13. Experiencia 4 opcional: RAG, 20 minutos adicionales

El taller base termina a las tres horas. Esta extensión se prepara como material posterior o requiere ampliar la sesión a tres horas y veinte minutos. El HTML la identifica como opcional. La solución completa del facilitador ya incluye la tercera herramienta; los equipos la añaden después de construir las dos herramientas base.

### Paso 1. Especificación, cuatro minutos

En la carpeta de práctica, abre `conocimiento/reglas-negocio.md`, `conocimiento/historial-defectos.md` y `conocimiento/severidad.md`. Son documentos ficticios. Define con `/especificar` el archivo `specs/rag.md`: buscar por palabras clave, devolver fuente y extracto, citar solo fuentes recuperadas y mantener el veredicto determinado por las pruebas. El núcleo `qa_core.py` del kit ya incluye la búsqueda.

**Avanza cuando** la consulta «operaciones gratuitas cobradas» debe devolver DEF-101 y una consulta ajena debe producir una lista vacía.

### Paso 2. Plan, tres minutos

Usa `/plan` y crea `specs/rag-plan.md` con tres tareas: conectar `buscar_contexto(consulta, tool_context)` al agente, añadir `sources` al esquema e instrucciones del revisor y mostrar las fuentes en el dashboard. Revisa que las consultas usen el conocimiento capturado al leer los criterios y acumulen citas en `tool_context.state['contexto']`. Una nueva ejecución reinicia esa lista.

**Avanza cuando** cada tarea identifica archivos y comprobación, y conserva el contrato de pruebas.

### Paso 3. Implementación, siete minutos

Invoca `/implementar` para cada tarea. La herramienta utiliza `Evidence.context`; los hallazgos incluyen `sources` y el reporte `context`. Renderiza las fuentes con `textContent`. En ADK Web pide revisar el motor con errores y abre Events para observar `buscar_contexto` después de las pruebas. Ejecuta desde la raíz de la práctica, con el entorno activo:

```powershell
.\taller.ps1 flujo
```

**Avanza cuando** el reporte identifica `mode: gemini`, las llamadas a herramientas y las fuentes recuperadas. Si la clave o cuota no están disponibles, usa `.\taller.ps1 flujo -Modo evidencia` para comprobar la recuperación local y deja pendiente la llamada real al modelo.

### Paso 4. Verificación, cuatro minutos

Restaura la versión con errores si ya la corregiste. Con los cuatro casos base deben seguir fallando QA-02 y QA-03, con 50 % aprobado. Si añadiste QA-05 tendrás cinco casos, tres fallas y 40 %. Comprueba que las fuentes de cada hallazgo aparecen en `context` y que el dashboard muestra sus extractos. Una fuente inventada debe provocar rechazo del reporte y conservar el último válido. Cambiar un documento debe generar otra identidad sin cambiar el motor ni el contrato.

**Avanza cuando** puedes explicar qué probaron las pruebas y qué información adicional aportó la base de conocimiento.

### Paso 5. Reto, dos minutos

Añade un documento o una sección `## DEF-120` con un defecto ficticio sobre el límite de 200 operaciones. Agrega un criterio de aceptación con un ID libre y verifica que una consulta sobre ese límite recupera la nueva fuente. Repite con una consulta ajena. Usa `/especificar`, revisa el plan y aplica `/verificar` para dejar evidencia del cambio.

**Entrega de la extensión**: spec, plan, tres herramientas, reporte con citas y dashboard con extractos. La recuperación por palabras clave está comprobada localmente. La calidad de las explicaciones de Gemini se valida al configurar la clave.
