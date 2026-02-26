@echo off

@REM set "INPUTDIR=%~1"
set "INPUTDIR=D:\Mosamatic\MartijnBroen\18-09-2025_42_monochrome\quarantine"

for %%F in ("%INPUTDIR%\*") do (
    echo Processing %%F
    call dcmdump ^
        +P FileMetaInformationVersion ^
        +P Modality ^
        +P ImageType ^
        +P SeriesDescription ^
        +P InstitutionName ^
        +P Manufacturer ^
        "%%F"
    echo ""
)