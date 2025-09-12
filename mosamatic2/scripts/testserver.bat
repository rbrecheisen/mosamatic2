@echo off

set /p CONFIRM="Is the server running? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting
    exit /b 1
)

poetry run pytest -s tests\miscellaneous\test_server.py