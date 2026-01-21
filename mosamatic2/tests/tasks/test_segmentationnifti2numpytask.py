from mosamatic2.core.tasks.segmentationnifti2numpytask.segmentationnifti2numpytask import SegmentationNifti2NumpyTask


def test_segmentationnifti2numpy():
    task = SegmentationNifti2NumpyTask(
        inputs={'segmentations': 'M:\\data\\mosamatic\\test\\L3'}, 
        params={'png': True},
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()