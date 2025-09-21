@echo off

set INPUT_FILE=D:\BOA\patient1.nii.gz
set WORKING_DIR=D:\BOA\work
set LOCAL_WEIGHTS_PATH=D:\BOA\weights

docker run ^
    --rm ^
    -v %INPUT_FILE%:/image.nii.gz ^
    -v %WORKING_DIR%:/workspace ^
    -v %LOCAL_WEIGHTS_PATH%:/app/weights ^
    --gpus all ^
    --network host ^
    --shm-size=8g --ulimit memlock=-1 --ulimit stack=67108864 ^
    --entrypoint /bin/sh ^
    shipai/boa-cli ^
    -c ^
    "python body_organ_analysis --input-image /image.nii.gz --output-dir /workspace/ --models all --verbose"