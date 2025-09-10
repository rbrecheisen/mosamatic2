@echo off

call mosamatic2-cli rescaledicomimages ^
    --images "D:\Mosamatic\CLI\Input\L3" ^
    --target_size 512 ^
    --output "D:\Mosamatic\CLI\Output" ^
    --overwrite true

call mosamatic2-cli segmentmusclefatl3tensorflow ^
    --images "D:\Mosamatic\CLI\Output\rescaledicomimagestask" ^
    --model_files "G:\My Drive\data\Mosamatic\models\tensorflow\L3\1.0" ^
    --output "D:\Mosamatic\CLI\Output" ^
    --overwrite true

call mosamatic2-cli calculatescores ^
    --images "D:\Mosamatic\CLI\Output\rescaledicomimagestask" ^
    --segmentations "D:\Mosamatic\CLI\Output\segmentmusclefatl3tensorflowtask" ^
    --file_type "npy" ^
    --output "D:\Mosamatic\CLI\Output" ^
    --overwrite true

call mosamatic2-cli createpngsfromsegmentations ^
    --segmentations "D:\Mosamatic\CLI\Output\segmentmusclefatl3tensorflowtask" ^
    --fig_width 10 ^
    --fig_height 10 ^
    --output "D:\Mosamatic\CLI\Output" ^
    --overwrite true
