import os
from mosamatic2.core.tasks import TotalSegmentatorTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'TotalSegmentatorTask'.lower()


def test_totalsegmentator():
    task = TotalSegmentatorTask(
        inputs={'scans': SOURCES['scans']}, 
        params={
            'tasks': 'total',
            'format': 'dicom',
        },
        output=SOURCES['output'],
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('scans')):        
        assert os.path.isfile(os.path.join(task.output(), f + '.nii.gz'))