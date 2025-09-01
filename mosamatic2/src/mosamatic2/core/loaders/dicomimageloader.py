import pydicom


from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.data.dicomimagedata import DicomImageData
from mosamatic2.core.utils import (
    is_dicom,
    load_dicom,
    is_jpeg2000_compressed,
)


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

    def load(self):
        if self.path():
            data = DicomImageData()
            data.set_path(self.path())
            if is_dicom(self.path()):
                p = load_dicom(self.path())
                if is_jpeg2000_compressed(p):
                    p.decompress()
                data.set_object(pydicom.dcmread(self.path()))
                return data
            return None
        raise RuntimeError('File path not set')