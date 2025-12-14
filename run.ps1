<#
Run the app using the project's virtualenv Python if present.
Usage: From PowerShell run `.
un.ps1` (no need to Activate.ps1).
#>
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venvPython = Join-Path $root '.venv\Scripts\python.exe'
<#
Run the app using the project's virtualenv Python if present.
Usage: From PowerShell run .\run.ps1 (no need to Activate.ps1).
#>
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venvPython = Join-Path $root '.venv\Scripts\python.exe'
if (Test-Path $venvPython) {
    & $venvPython (Join-Path $root 'app.py')
    exit $LASTEXITCODE
} else {
    Write-Host '.venv not found. Attempting system python...'
    python (Join-Path $root 'app.py')
}
