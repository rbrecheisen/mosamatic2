# mosamatic2-cli.exe showdoc defaultpipeline

$IMAGES_DIR = "M:\data\mosamatic\test\L3"
$MODEL_FILES_DIR = "M:\models\L3\tensorflow\1.0"
$OUTPUT_DIR = "M:\data\mosamatic\test\output"
$OVERWRITE = "true"

mosamatic2-cli.exe defaultpipeline --images ${IMAGES_DIR} --model_files ${MODEL_FILES_DIR} --output ${OUTPUT_DIR} --overwrite ${OVERWRITE}