class DicomImageSeriesData:
    def __init__(self):
        self._dir_path = None
        self._name = None
        self._images = []

    def path(self):
        return self._dir_path
    
    def set_path(self, path):
        self._dir_path = path

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def images(self):
        return self._images
    
    def load(self):
        pass