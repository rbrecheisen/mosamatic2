import os
import shutil
import numpy as np
from mosamatic2.core.tasks.task import Task
from scipy.ndimage import zoom


class RescaleDicomImagesTask(Task):
    INPUTS = ['images']
    PARAMS = ['width', 'height']

    def __init__(self, inputs, output, params):
        super(RescaleDicomImagesTask, self).__init__(inputs, output, params)

    def rescale_image(self):
        pass

    def run(self):
        pass