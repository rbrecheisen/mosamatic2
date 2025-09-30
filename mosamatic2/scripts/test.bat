@echo off

poetry run pytest -s ^
    --ignore=tests\test_server.py ^
    --ignore=tests\pipelines\test_defaultdockerpipeline.py ^
    --ignore=tests\pipelines\test_boadockerpipeline.py