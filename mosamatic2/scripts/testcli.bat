@echo off

@REM call mosamatic2-cli rescaledicomimages ^
@REM     --images "G:\My Drive\data\Mosamatic\testdata\L3" ^
@REM     --target_size 512 ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

@REM call mosamatic2-cli segmentmusclefatl3tensorflow ^
@REM     --images "G:\My Drive\data\Mosamatic\testdata\output\rescaledicomimagestask" ^
@REM     --model_files "G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0" ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

@REM call mosamatic2-cli calculatescores ^
@REM     --images "G:\My Drive\data\Mosamatic\testdata\output\rescaledicomimagestask" ^
@REM     --segmentations "G:\My Drive\data\Mosamatic\testdata\output\segmentmusclefatl3tensorflowtask" ^
@REM     --file_type "npy" ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

@REM call mosamatic2-cli createpngsfromsegmentations ^
@REM     --segmentations "G:\My Drive\data\Mosamatic\testdata\output\segmentmusclefatl3tensorflowtask" ^
@REM     --fig_width 10 ^
@REM     --fig_height 10 ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

@REM call mosamatic2-cli dicom2nifti ^
@REM     --images "G:\My Drive\data\Mosamatic\testdata\CT" ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

@REM call mosamatic2-cli selectslicefromscans ^
@REM     --scans "G:\My Drive\data\Mosamatic\testdata\CT" ^
@REM     --vertebra "L3" ^
@REM     --output "G:\My Drive\data\Mosamatic\testdata\output" ^
@REM     --overwrite true

call mosamatic2-cli defaultpipeline ^
    --images "G:\My Drive\data\Mosamatic\testdata\L3" ^
    --model_files "G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0" ^
    --output "G:\My Drive\data\Mosamatic\testdata\output" ^
    --overwrite true