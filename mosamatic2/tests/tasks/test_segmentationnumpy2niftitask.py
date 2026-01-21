from mosamatic2.core.tasks.segmentationnumpy2niftitask.segmentationnumpy2niftitask import SegmentationNumpy2NiftiTask


def test_segmentationnumpy2nifti():
    task = SegmentationNumpy2NiftiTask(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'segmentations': 'M:\\data\\mosamatic\\test\\L3'
        }, 
        params=None,
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()


if __name__ == '__main__':
    test_segmentationnumpy2nifti()