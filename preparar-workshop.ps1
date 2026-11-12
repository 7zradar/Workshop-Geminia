# Run once before the workshop from the downloaded repository.
[CmdletBinding()]
param(
    [ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$Equipo = 'equipo-01'
)
$ErrorActionPreference = 'Stop'

try {
    if ($env:OS -ne 'Windows_NT') { throw 'Este preparador requiere Windows y PowerShell 5.1 o superior.' }
    . (Join-Path $PSScriptRoot 'scripts\entorno.ps1')
    Update-WorkshopPath
    Write-Host '[1/5] Comprobando Python 3.12 y Node 22 o superior...'
    $basePython = Get-WorkshopPython
    $node = Get-WorkshopNode
    $missing = @()
    if (-not $basePython) { $missing += 'Python 3.12 (incluido el lanzador py)' }
    if (-not $node) { $missing += 'Node.js 22 o superior' }
    if ($missing.Count -gt 0) {
        throw ('Solicita a TI instalar: ' + ($missing -join '; ') + '. Despues cierra y abre Antigravity/PowerShell y repite este comando. No se instalaron herramientas del sistema.')
    }
    # Prefer the compatible Node just checked, even if an older Node comes first in PATH.
    $env:Path = (Split-Path -Parent $node.Path) + ';' + $env:Path

    Write-Host '[2/5] Creando o reanudando la practica sin sobrescribir tu trabajo...'
    & $basePython (Join-Path $PSScriptRoot 'scripts\preparar_practica.py') --equipo $Equipo --reanudar
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar la carpeta. Revisa el mensaje anterior; puedes elegir otro nombre con -Equipo.' }
    $practice = Join-Path $PSScriptRoot "practica\$Equipo"
    $practicePython = Join-Path $practice '.venv\Scripts\python.exe'
    Write-Host '[3/5] Preparando el entorno Python aislado...'
    if (-not (Test-Path -LiteralPath $practicePython -PathType Leaf)) {
        & $basePython -m venv (Join-Path $practice '.venv')
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear .venv. Comparte este error con TI.' }
    }
    & $practicePython -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 1)'
    if ($LASTEXITCODE -ne 0) { throw 'La practica tiene un entorno que no usa Python 3.12. Conserva esa carpeta y prepara otra con -Equipo equipo-02.' }

    $requirements = Join-Path $practice 'requirements.txt'
    Write-Host '[4/5] Instalando o reutilizando las dependencias del proyecto...'
    # pip reuses installed packages and enforces the versions pinned in requirements.txt.
    & $practicePython -m pip install --disable-pip-version-check -r $requirements
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron instalar dependencias. Revisa la conexion o solicita a TI acceso al repositorio Python autorizado. Puedes repetir el comando para reanudar.' }
    & $practicePython -m pip check
    if ($LASTEXITCODE -ne 0) { throw 'Hay dependencias incompatibles. Conserva el mensaje y solicita ayuda al facilitador.' }

    $configuration = Join-Path $practice '.env'
    if (-not (Test-Path -LiteralPath $configuration)) {
        Copy-Item -LiteralPath (Join-Path $practice '.env.example') -Destination $configuration
    }
    Write-Host '[5/5] Verificando herramientas, skills y pruebas locales sin API key...'
    & $practicePython (Join-Path $practice 'scripts\verificar_entorno.py')
    if ($LASTEXITCODE -ne 0) { throw 'La comprobacion no termino correctamente. Revisa el mensaje anterior y repite al resolverlo.' }

    Write-Host ''
    Write-Host 'PREPARACION COMPLETA' -ForegroundColor Green
    Write-Host "Abre esta carpeta en Antigravity: $practice"
    Write-Host 'No actives .venv manualmente: taller.ps1 usara el entorno preparado.'
    Write-Host 'Construye el agente siguiendo el HTML. Despues configura GOOGLE_API_KEY una sola vez en el .env de esa carpeta, antes de la primera llamada a Gemini.'
    Write-Host 'No se pidio ninguna clave ni se llamo a Gemini. Los agentes y la pagina se construyen durante el taller.'
    exit 0
} catch {
    Write-Host ('PREPARACION INCOMPLETA: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
