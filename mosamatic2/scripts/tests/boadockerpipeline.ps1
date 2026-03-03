# mosamatic2-cli.exe showdoc boadockerpipeline

$SCANS_DIR = "M:\data\mosamatic\test\CT\abdomen"
$OUTPUT_DIR = "M:\data\mosamatic\test\output"
$OVERWRITE = "true"

mosamatic2-cli.exe boadockerpipeline --scans ${SCANS_DIR} --output ${OUTPUT_DIR} --overwrite ${OVERWRITE}