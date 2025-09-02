import os
from mosamatic2.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask
from mosamatic2.core.utils import mosamatic_output_dir
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'RescaleDicomImagesTask'.lower()


def test_rescaledicomimages():
    task = RescaleDicomImagesTask(
        inputs={'images': SOURCES['input']}, 
        params={'target_size': 512}
    )
    task.run()
    found = False
    for d in os.listdir(mosamatic_output_dir()):
        dir_path = os.path.join(mosamatic_output_dir(), d)
        if TASK_NAME in dir_path:
            found = True
    assert found