import os
from mosamatic2.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask
from mosamatic2.core.utils import mosamatic_output_dir
from tests.sources import get_sources

SOURCES = get_sources()
TASK_NAME = 'RescaleDicomImagesTask'.lower()


def test_rescaledicomimages():
    task = RescaleDicomImagesTask(
        inputs={'images': SOURCES['input']}, 
        params={'target_size': 512},
        output=SOURCES['output'],
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('images')):
        if f.endswith('.dcm'):
            assert os.path.isfile(os.path.join(task.output(), f))