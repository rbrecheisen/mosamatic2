from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData


class MultiDicomImageData(Data, FileData):
    """
    MultiDicomImageData
    Represents multiple (2D) DICOM images, each of a different patient
    """
    def __init__(self):
        self._file_path = None
        self._name = None
        self._items = []

    def path(self):
        return self._file_path
    
    def set_path(self, path):
        self._file_path = path

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def items(self):
        return self._items
    
    def add_item(self, item):
        self._items.append(item)