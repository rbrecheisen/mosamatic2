@echo off

set VERSION=2.0.10
set IMAGES=G:\My Drive\data\Mosamatic\testdata\L3
set MODEL_FILES=G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0
set OUTPUT=G:\My Drive\data\Mosamatic\testdata\output

docker run --rm ^
    -v "%IMAGES%":/data/images ^
    -v "%MODEL_FILES%":/data/model_files ^
    -v "%OUTPUT%":/data/output ^
    brecheisen/mosamatic2-cli:%VERSION% defaultpipeline ^
        --images /data/images --model_files /data/model_files --output /data/output --overwrite true