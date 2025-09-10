import os
from mosamatic2.core.data.dicomimagedata import DicomImageData


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
        if self.path():
            images = []
            for f in os.listdir(self.path()):
                f_path = os.path.join(self.path(), f)
                image = DicomImageData()
                image.set_path(f_path)
                if image.load():
                    images.append(image)
            # Sort DICOM objects by instance number
            self._images = sorted(images, key=lambda image: int(image.object().get('InstanceNumber')))
            return True
        return False