import os
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.data.filedata import FileData
from mosamatic2.core.data.numpyimage import NumPyImage

LOG = LogManager()


class MultiNumPyImage(FileData):
    def __init__(self):
        super(MultiNumPyImage, self).__init__()
        self._images = []

    def images(self):
        return self._images
    
    def load(self):
        if self.path():
            for f in os.listdir(self.path()):
                f_path = os.path.join(self.path(), f)
                image = NumPyImage()
                image.set_path(f_path)
                if image.load():
                    self._images.append(image)
            return True
        return False