import os
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
    check_output(pipeline)


def check_output(pipeline):

    output_dir = os.path.join(pipeline.output(), 'rescaledicomimagestask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
    for f in os.listdir(output_dir):
        assert is_dicom(os.path.join(output_dir, f)), f'File {f} is not DICOM'

    task_name = 'segmentmusclefatl3pytorchtask' if pipeline.param('model_type') == 'pytorch' else 'segmentmusclefatl3tensorflowtask'
    output_dir = os.path.join(pipeline.output(), task_name)
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 4, 'Output directory does not contain 4 files'
    for f in os.listdir(output_dir):
        assert f.endswith('.seg.npy'), f'File {f} is not a NumPy file'

    output_dir = os.path.join(pipeline.output(), 'calculatescorestask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 2, 'Output directory does not contain 2 files'
    assert os.path.exists(os.path.join(output_dir, 'bc_scores.csv'))
    assert os.path.exists(os.path.join(output_dir, 'bc_scores.xlsx'))

    output_dir = os.path.join(pipeline.output(), 'createpngsfromsegmentationstask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 8, 'Output directory does not contain 8 files'