@echo off

poetry run pytest -s ^
    --ignore=tests\test_server.py