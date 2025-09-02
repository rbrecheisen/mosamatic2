import os

from mosamatic2.core.loaders.loader import Loader
from mosamatic2.core.loaders.fileloader import FileLoader
from mosamatic2.core.loaders.dicomimageloader import DicomImageLoader
from mosamatic2.core.data.dixonseriesdata import DixonSeriesData


class DixonSeriesLoader(Loader, FileLoader):
    def __init__(self):
        self._dir_path = None

    def path(self):
        return self._dir_path
    
    def set_path(self, path):
        self._dir_path = path

    def load(self):
        pass