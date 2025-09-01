from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData


class DicomSeriesData(Data, FileData):
    """
    DicomSeriesData
    Represents a single DICOM series, e.g., a CT or MRI scan
    """
    def __init__(self):
        self._dir_path = None
        self._name = None
        self._object = None

    def path(self):
        return self._dir_path
    
    def set_path(self, path):
        self._dir_path = path

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def object(self):
        return self._object
    
    def set_object(self, object):
        self._object = object