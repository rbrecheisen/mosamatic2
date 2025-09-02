from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData


class DixonSeriesData(Data, FileData):
    """
    DixonSeriesData
    Represents a set of Dixon MRI series for a single scan session. The
    set should contain in-phase, opposite-phase, water and fat series.
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

    def item(self):
        return self._object
    
    def set_item(self, object):
        self._object = object

    def ip(self):
        return self.item()['ip']
    
    def op(self):
        return self.item()['op']
    
    def water(self):
        return self.item()['water']
    
    def fat(self):
        return self.item()['fat']