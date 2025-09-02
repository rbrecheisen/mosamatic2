import os
import shutil
import numpy as np
from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.managers.datamanager import DataManager
from mosamatic2.core.data.multidicomimagedata import MultiDicomImageData
from mosamatic2.core.data.dicomimagedata import DicomImageData
from mosamatic2.core.utils import mosamatic_output_dir
from scipy.ndimage import zoom

LOG = LogManager()


class RescaleDicomImagesTask(Task):
    INPUTS = ['images']
    PARAMS = ['target_size']

    def __init__(self, inputs, params):
        super(RescaleDicomImagesTask, self).__init__(inputs, params)

    def rescale_image(self, p, target_size):
        pixel_array = p.pixel_array
        hu_array = pixel_array * p.RescaleSlope + p.RescaleIntercept
        hu_air = -1000
        new_rows = max(p.Rows, p.Columns)
        new_cols = max(p.Rows, p.Columns)
        padded_hu_array = np.full((new_rows, new_cols), hu_air, dtype=hu_array.dtype)
        padded_hu_array[:pixel_array.shape[0], :pixel_array.shape[1]] = hu_array
        pixel_array_padded = (padded_hu_array - p.RescaleIntercept) / p.RescaleSlope
        pixel_array_padded = pixel_array_padded.astype(pixel_array.dtype) # Image now has largest dimensions
        pixel_array_rescaled = zoom(pixel_array_padded, zoom=(target_size / new_rows), order=3) # Cubic interpolation
        pixel_array_rescaled = pixel_array_rescaled.astype(pixel_array.dtype)
        original_pixel_spacing = p.PixelSpacing
        new_pixel_spacing = [ps * (new_rows / target_size) for ps in original_pixel_spacing]
        p.PixelSpacing = new_pixel_spacing
        p.PixelData = pixel_array_rescaled.tobytes()
        p.Rows = target_size
        p.Columns = target_size
        return p

    def run(self):
        target_size = int(self.param('target_size'))
        data = self.input('images')
        assert isinstance(data, MultiDicomImageData)
        manager = DataManager()
        output_name = manager.add(MultiDicomImageData())
        output = manager.get(output_name)
        nr_steps = len(data.items())
        for step in range(nr_steps):
            source = data.items()[step]
            assert isinstance(source, DicomImageData)
            p = source.item()
            if len(p.pixel_array.shape) == 2:
                source_name = os.path.split(source.path())[1]
                if p.Rows != target_size or p.Columns != target_size:
                    p = self.rescale_image(p, target_size)
                    target = os.path.join(mosamatic_output_dir(), output_name, source_name)
                    p.save_as(target)
                    image = DicomImageData()
                    image.set_path(target)
                    image.set_item(p)
                    output.add_item(image)
                else:
                    # target = os.path.join(self.output(), source_name)
                    # shutil.copy(source, target)
                    pass
            else:
                LOG.warning(f'Shape of pixel data in file {source.path()} should be 2D but is {len(p.pixel_array.shape)}D')
            self.set_progress(step, nr_steps)