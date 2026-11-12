# Short commands for the participant, with no manual environment activation.
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('agente', 'flujo', 'automatizar', 'revisor')][string]$Accion,
    [ValidateSet('gemini', 'evidencia')][string]$Modo = 'gemini'
)
$ErrorActionPreference = 'Stop'
try {
    if ($Modo -eq 'evidencia' -and $Accion -in @('agente', 'revisor')) {
        throw 'El modo evidencia solo esta disponible para flujo y automatizar. Esta accion requiere Gemini.'
    }
    Set-Location -LiteralPath $PSScriptRoot
    . (Join-Path $PSScriptRoot 'scripts\entorno.ps1')
    Update-WorkshopPath
    $node = Get-WorkshopNode
    if (-not $node) { throw 'Falta Node 22 o superior. Solicita ayuda a TI y repite la preparacion.' }
    $env:Path = (Split-Path -Parent $node.Path) + ';' + $env:Path
    $pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $pythonPath)) {
        throw 'Abre la carpeta de practica indicada al terminar preparar-workshop.ps1. Si no completaste la preparacion, ejecutala primero desde el repositorio.'
    }
    if (-not (Test-Path -LiteralPath 'agente\agent.py')) { throw 'Primero construye agente/agent.py siguiendo el modulo 1 del HTML.' }
    if ($Accion -ne 'agente' -and -not (Test-Path -LiteralPath 'flujo\agent.py')) { throw 'Primero construye flujo/agent.py siguiendo el modulo 2 del HTML.' }
    switch ($Accion) {
        'agente' { & (Join-Path $PSScriptRoot '.venv\Scripts\adk.exe') web --port 8000 }
        'flujo' { & $pythonPath procesar.py --mode $Modo }
        'automatizar' { & $pythonPath servidor.py --mode $Modo --port 8767 }
        'revisor' { & $pythonPath scripts/probar_revisor.py }
    }
    exit $LASTEXITCODE
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
