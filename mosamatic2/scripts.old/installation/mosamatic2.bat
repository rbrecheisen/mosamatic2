@echo off
setlocal EnableExtensions

@rem configuration
set "INSTALL_DIR=%LOCALAPPDATA%\Miniforge3"
set "ENV_NAME=mosamatic2"
set "ENV_DIR=%INSTALL_DIR%\envs\%ENV_NAME%"
set "APP_EXE=%ENV_DIR%\Scripts\mosamatic2.exe"
set "CONDA_BAT=%INSTALL_DIR%\condabin\conda.bat"

if not exist "%CONDA_BAT%" (
  echo ERROR: Miniforge not found at "%INSTALL_DIR%".
  echo Please run the installer first.
  pause
  exit /b 1
)

if not exist "%APP_EXE%" (
  echo ERROR: "%APP_EXE%" not found.
  pause
  exit /b 1
)

echo Running %ENV_NAME%...
"%APP_EXE%" %*
if errorlevel 1 (
  echo ERROR: Could not run mosamatic2.
  echo Press any key to continue...
  pause
  exit /b 1
)