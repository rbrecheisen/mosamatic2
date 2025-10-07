import os
from mosamatic2.core.pipelines import LiverAnalysisPipeline
from tests.sources import get_sources

SOURCES = get_sources()


def test_liveranalysispipeline():
    assert os.path.exists(SOURCES['scans']), 'Input directory does not exist'
    pipeline = LiverAnalysisPipeline(
        inputs={'scans': 'D:\\Mosamatic\\TestData\\CT'},
        params={'compressed': True},
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    pipeline.run()
    check_output(pipeline)


def check_output(pipeline):
    output_dir = os.path.join(pipeline.output(), 'dicom2niftitask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 1, 'Output directory does not contain 1 file'
    for f in os.listdir(output_dir):
        assert f.endswith('.nii.gz')
        
    output_dir = os.path.join(pipeline.output(), 'totalsegmentatortask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 8, 'Output directory does not contain 8 files'
    for f in os.listdir(output_dir):
        assert f.endswith('.nii.gz')
        assert f.startswith('patient1_')

    output_dir = os.path.join(pipeline.output(), 'calculatemaskstatisticstask')
    assert os.path.exists(output_dir), 'Output directory does not exist'
    assert len(os.listdir(output_dir)) == 10, 'Output directory does not contain 8 files'
    files = os.listdir(output_dir)
    for i in range(8):
        assert f'patient1_liver_segment_{i+1}.nii.gz.png' in files
    assert 'statistics.csv' in files and 'statistics.xlsx' in files