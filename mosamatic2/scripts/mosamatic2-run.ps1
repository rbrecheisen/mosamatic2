#requires -Version 5.1
$ErrorActionPreference = "Stop"

# Configuration
$INSTALL_DIR = Join-Path $env:LOCALAPPDATA "miniforge3"
$ENV_NAME    = "mosamatic2"
$ENV_DIR     = Join-Path $INSTALL_DIR "envs\$ENV_NAME"
$CONDA_BAT   = Join-Path $INSTALL_DIR "condabin\conda.bat"

function Invoke-Conda {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Arguments,

        [switch]$IgnoreExitCode,
        [switch]$Quiet
    )

    if (-not (Test-Path $CONDA_BAT)) {
        throw "conda.bat not found at: $CONDA_BAT"
    }

    $cmdLine = "call `"$CONDA_BAT`" $Arguments"
    if ($Quiet) {
        cmd.exe /d /c $cmdLine *> $null
    } else {
        cmd.exe /d /c $cmdLine
    }

    $exit = $LASTEXITCODE
    if (-not $IgnoreExitCode -and $exit -ne 0) {
        throw "Conda command failed (exit $exit): $Arguments"
    }

    return $exit
}

if (-not (Test-Path $CONDA_BAT)) {
    Write-Host "ERROR: Miniforge not found at `"$INSTALL_DIR`"." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Optional sanity check (path exists)
if (-not (Test-Path $ENV_DIR)) {
    Write-Host "ERROR: Environment folder not found: `"$ENV_DIR`"." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Sanity check: is PySide6 importable in this env?
try {
    Invoke-Conda "run -n `"$ENV_NAME`" python -c `"import PySide6`"" -Quiet | Out-Null
} catch {
    Write-Host "ERROR: PySide6 is not importable in env `"$ENV_NAME`"." -ForegroundColor Red
    Write-Host "Try: conda list pyside6"
    Write-Host 'Or:  python -c "import sys; print(sys.executable)"'
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Running $ENV_NAME..."

# Run the app, forwarding all PowerShell script arguments to the executable
$forwardedArgs = @()
foreach ($a in $args) {
    # Quote each arg safely for cmd.exe
    $escaped = $a -replace '"', '\"'
    $forwardedArgs += "`"$escaped`""
}
$argString = ($forwardedArgs -join ' ')

cmd.exe /d /c "call `"$CONDA_BAT`" run --no-capture-output -n `"$ENV_NAME`" $ENV_NAME $argString"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not run Mosamatic2" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}