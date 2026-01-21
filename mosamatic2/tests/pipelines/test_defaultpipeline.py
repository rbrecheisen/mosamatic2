from mosamatic2.core.pipelines import DefaultPipeline
from mosamatic2.core.utils import is_dicom


def test_defaultpipeline():
    pipeline = DefaultPipeline(
        inputs={
            'images': 'M:\\data\\mosamatic\\test\\L3',
            'model_files': 'M:\\models\\L3\\tensorflow\\1.0',
        },
        params={
            'target_size': 512,
            'model_type': 'tensorflow',
            'model_version': 1.0,
            'file_type': 'npy',
            'fig_width': 10,
            'fig_height': 10,
            'hu_low': 30,
            'hu_high': 150,
            'alpha': 1.0,
        },
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    pipeline.run()