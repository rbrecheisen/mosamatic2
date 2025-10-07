import os
from mosamatic2.core.tasks import TotalSegmentatorTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'TotalSegmentatorTask'.lower()


def test_totalsegmentator():
    task = TotalSegmentatorTask(
        inputs={'scans': 'D:\\Mosamatic\\TestData\\CT'}, 
        params={
            'tasks': 'total',
            'format': 'dicom',
        },
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()