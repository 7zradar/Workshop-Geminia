param(
    [ValidateSet('evidencia', 'gemini')][string]$Modo = 'evidencia',
    [int]$Puerto = 8765
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw 'Instale Node 22 o superior antes de iniciar la demo.'
}
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$parentPython = Join-Path (Split-Path $PSScriptRoot -Parent) '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    if (Test-Path -LiteralPath $parentPython) {
        $pythonPath = $parentPython
    } else {
        py -3.12 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno. Instale Python 3.12.' }
    }
}
& $pythonPath -c 'import google.adk' 2>$null
if ($LASTEXITCODE -ne 0) {
    & $pythonPath -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron instalar las dependencias.' }
}
if (-not (Test-Path -LiteralPath '.env')) {
    Copy-Item -LiteralPath '.env.example' -Destination '.env'
}
Write-Host "Dashboard http://127.0.0.1:$Puerto/"
Write-Host "Presentacion http://127.0.0.1:$Puerto/presentacion"
& $pythonPath servidor.py --mode $Modo --port $Puerto
