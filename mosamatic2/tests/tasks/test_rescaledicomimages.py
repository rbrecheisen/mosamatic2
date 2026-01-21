import os
from mosamatic2.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask


def test_rescaledicomimages():
    task = RescaleDicomImagesTask(
        inputs={'images': 'M:\\data\\mosamatic\\test\\L3'}, 
        params={'target_size': 512},
        output='M:\\data\\mosamatic\\test\\output',
        overwrite=True,
    )
    task.run()
    for f in os.listdir(task.input('images')):
        if f.endswith('.dcm'):
            assert os.path.isfile(os.path.join(task.output(), f))