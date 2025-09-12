@echo off

poetry run pytest -s ^
    --ignore=tests\miscellaneous\test_server.py ^
    --ignore=tests\experiments