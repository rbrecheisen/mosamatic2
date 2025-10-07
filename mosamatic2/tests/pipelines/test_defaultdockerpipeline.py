import os

from mosamatic2.core.pipelines import DefaultDockerPipeline
from mosamatic2.core.utils import is_dicom
from tests.sources import get_sources

SOURCES = get_sources()
VERSION = '2.0.16'


def test_defaultdockerpipeline():
    pipeline = DefaultDockerPipeline(
        inputs={
            'images': 'D:\\Mosamatic\\TestData\\L3',
            'model_files': 'D:\\Mosamatic\\TensorFlowModelFiles',
        },
        params={'version': VERSION},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    pipeline.run()
    # check_output(pipeline)


def check_output(pipeline):

    output_dir = os.path.join(pipeline.output(), 'defaultpipeline/rescaledicomimagestask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
    for f in os.listdir(output_dir):
        assert is_dicom(os.path.join(output_dir, f)), f'File {f} is not DICOM'

    task_name = 'segmentmusclefatl3pytorchtask' if pipeline.param('model_type') == 'pytorch' else 'segmentmusclefatl3tensorflowtask'
    output_dir = os.path.join(pipeline.output(), 'defaultpipeline/' + task_name)
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
    for f in os.listdir(output_dir):
        assert f.endswith('.seg.npy'), f'File {f} is not a NumPy file'

    output_dir = os.path.join(pipeline.output(), 'defaultpipeline/calculatescorestask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 2, 'Output directory does not contain 2 files'
    assert os.path.exists(os.path.join(output_dir, 'bc_scores.csv'))
    assert os.path.exists(os.path.join(output_dir, 'bc_scores.xlsx'))

    output_dir = os.path.join(pipeline.output(), 'defaultpipeline/createpngsfromsegmentationstask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
    for f in os.listdir(output_dir):
        assert f.endswith('.seg.npy.png'), f'File {f} is not a PNG file'