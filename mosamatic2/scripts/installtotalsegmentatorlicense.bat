@echo off

setlocal

set /p KEY=<C:\Users\r.brecheisen\totalsegmentator-license.txt

call totalseg_set_license -l %KEY%

endlocal