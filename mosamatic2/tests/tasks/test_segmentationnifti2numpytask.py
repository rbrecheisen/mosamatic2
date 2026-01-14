import os
from mosamatic2.core.tasks.segmentationnifti2numpytask.segmentationnifti2numpytask import SegmentationNifti2NumpyTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'SegmentationNumpy2NiftiTask'.lower()


def test_segmentationnifti2numpy():
    task = SegmentationNifti2NumpyTask(
        inputs={'segmentations': 'D:\\Mosamatic\\TestData\\output\\segmentationnumpy2niftitask'}, 
        params={'png': True},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()