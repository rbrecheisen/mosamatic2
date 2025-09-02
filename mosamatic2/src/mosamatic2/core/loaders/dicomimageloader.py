from mosamatic2.core.managers.logmanager import LogManager
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
    def __init__(self):
        self._file_path = None
        
    def path(self):
        return self._file_path
    
    def set_path(self, path):
        self._file_path = path

    def load(self):        
        if self.path():
            if is_dicom(self.path()):
                p = load_dicom(self.path())
                if is_jpeg2000_compressed(p):
                    p.decompress()
                data = DicomImageData()
                data.set_path(self.path())
                data.set_item(p)
                return data
            return None
        raise RuntimeError('File path not set')