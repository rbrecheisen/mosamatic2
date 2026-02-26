#requires -Version 5.1
$ErrorActionPreference = "Stop"

# Configuration
$MINIFORGE_URL  = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
$INSTALL_DIR    = Join-Path $env:LOCALAPPDATA "Miniforge3"
$ENV_NAME       = "mosamatic2"
$PYTHON_VERSION = "3.11"

# Internal settings
$CONDA_INSTALLED = $false
$TMP_DIR         = Join-Path $env:TEMP "miniforge_bootstrap"
$MINIFORGE_EXE   = Join-Path $TMP_DIR "Miniforge3-Windows-x86_64.exe"
$CONDA_BAT       = Join-Path $INSTALL_DIR "condabin\conda.bat"

function Invoke-Conda {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Arguments,

        [switch]$IgnoreExitCode
    )

    if (-not (Test-Path -LiteralPath $script:CONDA_BAT)) {
        throw "conda.bat not found at: $CONDA_BAT"
    }

    $cmdLine = "call `"$CONDA_BAT`" $Arguments"
    cmd.exe /d /c $cmdLine
    $exit = $LASTEXITCODE

    if (-not $IgnoreExitCode -and $exit -ne 0) {
        throw "Conda command failed (exit $exit): $Arguments"
    }

    return $exit
}

New-Item -ItemType Directory -Force -Path $TMP_DIR | Out-Null

Write-Host "Checking if Miniforge already installed..."
if (Test-Path -LiteralPath $CONDA_BAT) {
    Write-Host "Miniforge already installed in $INSTALL_DIR"
    Write-Host "Skipping installation..."
    $CONDA_INSTALLED = $true
}

if (-not $CONDA_INSTALLED) {
    Write-Host "Downloading Miniforge..."
    & curl.exe -L --fail --retry 3 --retry-delay 2 -o $MINIFORGE_EXE $MINIFORGE_URL
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to download Miniforge." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host "Installing Miniforge silently..."
    $proc = Start-Process -FilePath $MINIFORGE_EXE `
        -ArgumentList '/S', "/D=$INSTALL_DIR" `
        -Wait -PassThru

    if ($proc.ExitCode -ne 0) {
        Write-Host "ERROR: Miniforge installer failed with exit code $($proc.ExitCode)." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

$maxSeconds = 30
$elapsed = 0
while (-not (Test-Path -LiteralPath $CONDA_BAT) -and $elapsed -lt $maxSeconds) {
    Start-Sleep -Seconds 1
    $elapsed++
}

Write-Host "Initializing conda (CONDA_BAT=$CONDA_BAT)"
Invoke-Conda 'init powershell' | Out-Null
Invoke-Conda 'config --set always_yes yes --set changeps1 no' | Out-Null
Invoke-Conda 'config --set auto_activate false' | Out-Null

Write-Host "Creating/refreshing env `"$ENV_NAME`" with Python $PYTHON_VERSION..."
Invoke-Conda "env remove -n `"$ENV_NAME`"" -IgnoreExitCode | Out-Null
Invoke-Conda "create -n `"$ENV_NAME`" python=$PYTHON_VERSION pip twine setuptools wheel python-build tomlkit -c conda-forge"

Write-Host "Installing `"$ENV_NAME`"..."
Invoke-Conda "run -n `"$ENV_NAME`" python -m pip install `"$ENV_NAME`""

Write-Host "Done." -ForegroundColor Green
Read-Host "Press Enter to exit"