from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData


class DicomImageData(Data, FileData):
    """
    DicomImageData
    Represents a single (2D) DICOM image
    """
    def __init__(self):
        self._file_path = None
        self._name = None
        self._item = None

    def path(self):
        return self._file_path
    
    def set_path(self, path):
        self._file_path = path

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def item(self):
        return self._item
    
    def set_item(self, item):
        self._item = item