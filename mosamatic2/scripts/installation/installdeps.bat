@echo off

@rem Make sure activate the mosamatic2 environment before running
@rem the command below!
call mamba install -c conda-forge ^
    poetry ^
    pyside6 ^
    numpy ^
    pandas ^
    nibabel ^
    dicom2nifti ^
    openpyxl ^
    pendulum ^
    pydicom ^
    pillow ^
    scipy ^
    matplotlib ^
    simpleitk ^
    vtk