# Preparación del participante con un comando

## Usuario y objetivo
Un participante en Windows abre el repositorio descargado y ejecuta `powershell -NoProfile -ExecutionPolicy Bypass -File .\preparar-workshop.ps1`. La preparación termina antes del taller. Antigravity sigue siendo la herramienta con la que construye los agentes y el dashboard durante la sesión.

## Alcance
El script comprueba Python 3.12 y Node 22 o superior. Por decisión del usuario, no instala herramientas del sistema: indica qué falta para que TI lo instale. Antigravity y su inicio de sesión también se preparan previamente. Git no es necesario si el repositorio se descarga como ZIP. No cambia la política de ejecución de PowerShell.

Crea `practica/equipo-01` (nombre configurable), prepara su entorno `.venv`, instala sus dependencias y comprueba el runner y las skills. Crea `.env` con la clave vacía solo si no existe. No pide, lee ni valida credenciales de Gemini, no llama a la API y no construye los entregables del taller.

La preparación se puede reanudar en un kit marcado como propio. Solo agrega archivos ausentes, conserva código, contratos, skills y `.env` existentes, y no reinicia el motor. Rechaza carpetas existentes sin la marca de kit. La comprobación informa de las fallas pedagógicas sin tratarlas como un fallo de instalación. El informe local `salida/preparacion.json` acredita el entorno, no una llamada a Gemini.

## Durante el taller
El kit incluye `taller.ps1` con acciones `agente`, `flujo`, `automatizar` y `revisor`. Usa directamente los ejecutables de `.venv` sin activar el entorno manualmente. Comprueba que el participante haya construido el componente antes de ejecutarlo. La API key se configura una vez, después de construir el primer agente y antes de su primera llamada a Gemini. El dashboard reutiliza el servidor del bloque 2.

## Criterios de aceptación
| ID | Acción | Resultado esperado |
|---|---|---|
| E1 | Preparar desde una ruta con espacios | Un comando crea un kit utilizable y un entorno aislado |
| E2 | Preparar sin API key | Éxito sin llamadas a Gemini; `.env` vacío y agentes/página sin construir |
| E3 | Verificar el kit nuevo | ADK y dependencias importables, tres skills presentes, runner con 2/4 y 50 % identificado como esperado |
| E4 | Repetir tras editar código, contrato, skill y `.env` | Conserva los archivos y reutiliza dependencias si no cambiaron |
| E5 | Reanudar una preparación interrumpida | Agrega archivos ausentes sin sobrescribir archivos existentes |
| E6 | Carpeta ajena, nombre inválido o entorno incompatible | Error claro y código distinto de cero; no declara el entorno listo |
| E7 | Herramienta ausente | Informa qué debe instalar TI, sin intentar instalar herramientas ni declarar el entorno listo |
| E8 | Ejecutar el agente sin construirlo | Mensaje que dirige al módulo correspondiente, sin activar el entorno manualmente |
| E9 | Seguir el HTML | Un comando previo, clave una sola vez, mismos 180 minutos y servidor reutilizado en el bloque 3 |

## Límites de validación
Las comprobaciones de rutas, conservación de archivos y errores se automatizan. La instalación de dependencias se ensaya en este equipo con Python y Node ya presentes. Las políticas corporativas de instalación, red y ejecución requieren un ensayo previo con TI. El script no elude esas políticas.
