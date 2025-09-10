import os
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.loaders.dicomimageloader import DicomImageLoader
from mosamatic2.core.data.multidicomimagedata import MultiDicomImageData

LOG = LogManager()


class MultiDicomImageLoader(Loader, FileLoader):
    def __init__(self):
        self._file_path = None

    def path(self):
        return self._file_path
    
    def set_path(self, path):
        self._file_path = path

    def load(self):
        series_instance_uids = []
        if self.path():
            items = []
            for f in os.listdir(self.path()):
                f_path = os.path.join(self.path(), f)
                loader = DicomImageLoader()
                loader.set_path(f_path)
                image = loader.load()
                if image:
                    series_instance_uid = image.object().SeriesInstanceUID
                    if series_instance_uid in series_instance_uids:
                        RuntimeError('Cannot load DICOM images with identical series instance UID')
                    items.append(image)
            data = MultiDicomImageData()
            for item in items:
                data.add_image(item)
            return data
        raise RuntimeError('Path not set')