import os
from mosamatic2.core.tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'CreatePngsFromSegmentationsTask'.lower()


def test_createpngsfromsegmentationstask():
    task = CreatePngsFromSegmentationsTask(
        inputs={
            'images': 'D:\\Mosamatic\\TestData\\L3',
            'segmentations': 'D:\\Mosamatic\\TestData\\L3'
        }, 
        params={
            'fig_width': 10, 
            'fig_height': 10,
            'hu_low': 30,
            'hu_high': 150,
            'alpha': 1.0,
        },
        output='D:\\Mosamatic\\TestData\\output',
        overwrite=True,
    )
    task.run()