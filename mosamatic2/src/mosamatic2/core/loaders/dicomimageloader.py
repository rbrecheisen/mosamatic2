import pydicom


from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.managers.datamanager import DataManager
from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.data.dicomimagedata import DicomImageData
from mosamatic2.core.utils import (
    is_dicom,
    load_dicom,
    is_jpeg2000_compressed,
)

LOG = LogManager()


class DicomImageLoader(Loader, FileLoader):
    """
    DicomImageLoader
    Loads a single DICOM image
    """
    def __init__(self):
        self._file_path = None
        
    def path(self):
        return self._file_path
    
    def set_path(self, path):
        self._file_path = path

    def load(self, to_manager=True):        
        if self.path():
            if is_dicom(self.path()):
                p = load_dicom(self.path())
                if is_jpeg2000_compressed(p):
                    p.decompress()
                data = DicomImageData()
                data.set_path(self.path())
                data.set_item(p)
                if to_manager:
                    manager = DataManager()
                    manager.add(data)
                return data
            return None
        raise RuntimeError('File path not set')