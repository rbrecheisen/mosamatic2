@echo off

setlocal

if "%~1"=="" (
    call scripts\test.bat
)

set /p CONFIRM="Did the tests run without errors? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

set /p BUMP_LEVEL="What version bump level do you want to use? [major, minor, patch (default)] "
if /I "%BUMP_LEVEL%"=="major" (
    poetry version major
) else if /I "%BUMP_LEVEL%"=="minor" (
    poetry version minor
) else (
    poetry version patch
)

FOR /F %%v IN ('poetry version --short') DO SET VERSION=%%v
echo %VERSION% > src\mosamatic2\ui\resources\VERSION
echo Deploying version %VERSION% to PyPI...
set /p CONFIRM="Is this correct? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

set /p TOKEN=<"G:\My Drive\data\ApiKeysAndPasswordFiles\pypi-token.txt"

poetry publish --build --username __token__ --password %TOKEN%

@REM set /p CONFIRM="Do you also want to build and deploy a Docker image of mosamatic2? (y/n) "
@REM if /I NOT "%CONFIRM%"=="y" (
@REM     echo Aborting deployment
@REM     exit /b 1
@REM )
@REM call scripts\builddockerimage.bat
@REM call scripts\deploy2dockerhub.bat

endlocal