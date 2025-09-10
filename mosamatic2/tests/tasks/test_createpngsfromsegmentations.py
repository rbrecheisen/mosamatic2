import os
from mosamatic2.core.tasks.createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'CreatePngsFromSegmentationsTask'.lower()


def test_createpngsfromsegmentationstask():
    task = CreatePngsFromSegmentationsTask(
        inputs={'segmentations': SOURCES['input']}, 
        params={'fig_width': 10, 'fig_height': 10},
        output=SOURCES['output'],
        overwrite=True,
    )
    task.run()