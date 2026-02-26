@echo off

@REM Make sure activate the mosamatic2 environment before running
@REM the command below!
call mamba install -c conda-forge poetry pyside6
@REM call mamba install -c conda-forge ^
@REM     poetry ^
@REM     pyside6 ^
@REM     numpy ^
@REM     pandas ^
@REM     nibabel ^
@REM     dicom2nifti ^
@REM     openpyxl ^
@REM     pendulum ^
@REM     pydicom ^
@REM     pillow ^
@REM     scipy ^
@REM     matplotlib ^
@REM     simpleitk ^
@REM     vtk