import os
from mosamatic2.core.tasks.rescaledicomimagestask.rescaledicomimagestask import RescaleDicomImagesTask
from mosamatic2.core.loaders.multidicomimageloader import MultiDicomImageLoader
from mosamatic2.core.data.multidicomimagedata import MultiDicomImageData
from mosamatic2.core.data.dicomimagedata import DicomImageData
from tests.sources import get_sources

SOURCES = get_sources()
IMAGES_DIR = ''


def test_rescaledicomimages():
    images_dir = SOURCES['input']
    task = RescaleDicomImagesTask(
        inputs={'images': images_dir}, 
        params={'target_size': 512}
    )
    task.run()
    # images_loader = MultiDicomImageLoader()
    # images_loader.set_path(images_path)
    # data = images_loader.load()
    # assert isinstance(data, MultiDicomImageData)
    # for image in data.items():
    #     assert isinstance(image, DicomImageData)
    # task = RescaleDicomImagesTask(inputs={'images': data}, params={'target_size': 512})
    # task.run()