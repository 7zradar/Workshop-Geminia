# Shared by preparation and the participant launcher. Compatible with Windows PowerShell 5.1.
function Update-WorkshopPath {
    $extraPaths = @(
        [Environment]::GetEnvironmentVariable('Path', 'Machine'),
        [Environment]::GetEnvironmentVariable('Path', 'User'),
        (Join-Path $env:ProgramFiles 'nodejs')
    )
    $env:Path = (@($env:Path) + $extraPaths | Where-Object { $_ }) -join ';'
}

function Get-WorkshopPython {
    $candidates = @()
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        try {
            $selected = & $launcher.Source -3.12 -c 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0) { $candidates += $selected }
        } catch { }
    }
    $candidates += @(Get-Command python.exe, python3.exe -All -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty Source)
    $candidates += Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
    foreach ($candidate in ($candidates | Select-Object -Unique)) {
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
        # Skip Store aliases that open an installer rather than running Python.
        if ($candidate -match '\\Microsoft\\WindowsApps\\python[^\\]*\.exe$') { continue }
        try {
            $result = & $candidate -c 'import sys; print(sys.executable) if sys.version_info[:2] == (3, 12) else sys.exit(1)' 2>$null
            if ($LASTEXITCODE -eq 0 -and $result) { return [string]$result }
        } catch { }
    }
    return $null
}

function Get-WorkshopNode {
    foreach ($command in @(Get-Command node.exe -All -ErrorAction SilentlyContinue)) {
        try {
            $version = & $command.Source --version 2>$null
            if ($LASTEXITCODE -eq 0 -and $version -match '^v(\d+)\.') {
                if ([int]$Matches[1] -ge 22) {
                    return [pscustomobject]@{ Path = $command.Source; Version = [string]$version }
                }
            }
        } catch { }
    }
    return $null
}
