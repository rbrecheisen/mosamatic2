import os
from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.loaders.dicomimageloader import DicomImageLoader
from mosamatic2.core.data.dicomseriesdata import DicomSeriesData


class DicomSeriesLoader(Loader, FileLoader):
    def __init__(self):
        self._dir_path = None

    def path(self):
        return self._dir_path
    
    def set_path(self, path):
        self._dir_path = path

    def load(self):
        if self.path():
            data = DicomSeriesData()
            data.set_path(self.path())
            items = []
            for f in os.listdir(self.path()):
                f_path = os.path.join(self.path(), f)
                loader = DicomImageLoader()
                loader.set_path(f_path)
                file_data = loader.load()
                if file_data:
                    items.append(file_data)
            # Sort DICOM objects by instance number
            items_sorted = sorted(items, key=lambda item: int(item.item().get('InstanceNumber')))
            for item in items_sorted:
                data.add_item(item)
            return data
        raise RuntimeError('Directory path not set')