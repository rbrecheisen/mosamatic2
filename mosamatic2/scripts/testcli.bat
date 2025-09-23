@echo off

call mosamatic2-cli rescaledicomimages ^
    --images "G:\My Drive\data\Mosamatic\testdata\L3" ^
    --target_size 512 ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli segmentmusclefatl3tensorflow ^
    --images "G:\My Drive\data\Mosamatic\testdata\output\rescaledicomimagestask" ^
    --model_files "G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli calculatescores ^
    --images "G:\My Drive\data\Mosamatic\testdata\output\rescaledicomimagestask" ^
    --segmentations "G:\My Drive\data\Mosamatic\testdata\output\segmentmusclefatl3tensorflowtask" ^
    --file_type "npy" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli createpngsfromsegmentations ^
    --segmentations "G:\My Drive\data\Mosamatic\testdata\output\segmentmusclefatl3tensorflowtask" ^
    --fig_width 10 ^
    --fig_height 10 ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli dicom2nifti ^
    --images "G:\My Drive\data\Mosamatic\testdata\CT" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli selectslicefromscans ^
    --scans "G:\My Drive\data\Mosamatic\testdata\CT" ^
    --vertebra "L3" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true

call mosamatic2-cli defaultpipeline ^
    --images "G:\My Drive\data\Mosamatic\testdata\L3" ^
    --model_files "G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true