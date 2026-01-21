import os
from mosamatic2.core.tasks.dicom2niftitask.dicom2niftitask import Dicom2NiftiTask


def test_dicom2nifti():
    task = Dicom2NiftiTask(
        inputs={'scans': 'M:\\data\\mosamatic\\test\\CT\\abdomen'}, 
        params={'compressed': True},
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('scans')):        
        assert os.path.isfile(os.path.join(task.output(), f + '.nii.gz'))