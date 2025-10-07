import os
from mosamatic2.core.tasks.dicom2niftitask.dicom2niftitask import Dicom2NiftiTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'Dicom2NiftiTask'.lower()


def test_dicom2nifti():
    task = Dicom2NiftiTask(
        inputs={'scans': 'D:\\Mosamatic\\TestData\\CT'}, 
        params={'compressed': True},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('scans')):        
        assert os.path.isfile(os.path.join(task.output(), f + '.nii.gz'))