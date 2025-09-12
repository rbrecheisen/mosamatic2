import os
import requests
from tests.sources import get_sources

SOURCES = get_sources()


def test_server():
    result = requests.get('http://localhost:8000/rescaledicomimages', params={
        'images': SOURCES['input'],
        'target_size': 512,
        'output': SOURCES['output'],
        'overwrite': True,
    })
    assert result.status_code == 200
    result = requests.get('http://localhost:8000/segmentmusclefatl3tensorflow', params={
        'images': os.path.join(SOURCES['output'], 'rescaledicomimagestask'),
        'model_files': SOURCES['model_files']['tensorflow'],
        'output': SOURCES['output'],
        'overwrite': True,
    })
    assert result.status_code == 200
    result = requests.get('http://localhost:8000/calculatescores', params={
        'images': os.path.join(SOURCES['output'], 'rescaledicomimagestask'),
        'segmentations': os.path.join(SOURCES['output'], 'segmentmusclefatl3tensorflowtask'),
        'file_type': 'npy',
        'output': SOURCES['output'],
        'overwrite': True,
    })
    assert result.status_code == 200
    result = requests.get('http://localhost:8000/createpngsfromsegmentations', params={
        'segmentations': os.path.join(SOURCES['output'], 'segmentmusclefatl3tensorflowtask'),
        'fig_width': 10,
        'fig_height': 10,
        'output': SOURCES['output'],
        'overwrite': True,
    })
    assert result.status_code == 200
    result = requests.get('http://localhost:8000/dicom2nifti', params={
        'segmentations': os.path.join(SOURCES['output'], 'segmentmusclefatl3tensorflowtask'),
        'fig_width': 10,
        'fig_height': 10,
        'output': SOURCES['output'],
        'overwrite': True,
    })
    assert result.status_code == 200