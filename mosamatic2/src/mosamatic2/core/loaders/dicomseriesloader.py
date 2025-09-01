import os

from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.loaders.dicomimageloader import DicomImageLoader
from mosamatic2.core.data.dicomseriesdata import DicomSeriesData


class DicomSeriesLoader(Loader, FileLoader):
    """
    DicomSeriesLoader
    Loads a single DICOM image series, e.g., a single CT or MRI
    scan. For multi-series DICOM data like Dixon MRI, you need a
    specific loader, e.g., DixonSeriesLoader
    """
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
            object = []
            for f in os.listdir(self.path()):
                f_path = os.path.join(self.path(), f)
                loader = DicomImageLoader()
                loader.set_path(f_path)
                file_data = loader.load() # Returns None if not DICOM
                if file_data:
                    object.append(file_data)
            # Sort DICOM objects by instance number
            object_sorted = sorted(object, key=lambda item: int(item.object().get('InstanceNumber')))
            data.set_object(object_sorted)
            return data
        raise RuntimeError('Directory path not set')