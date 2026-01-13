import os
from mosamatic2.core.tasks.segmentationnumpy2niftitask.segmentationnumpy2niftitask import SegmentationNumpy2NiftiTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'SegmentationNumpy2NiftiTask'.lower()


def test_segmentationnumpy2nifti():
    task = SegmentationNumpy2NiftiTask(
        inputs={'segmentations': 'D:\\Mosamatic\\TestData\\output\\segmentmusclefatl3tensorflowtask'}, 
        params=None,
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()