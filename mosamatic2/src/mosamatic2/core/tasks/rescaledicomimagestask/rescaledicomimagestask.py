import os
import shutil
from mosamatic2.core.tasks.task import Task


class RescaleDicomImagesTask(Task):
    def __init__(self, inputs, output, params):
        super(RescaleDicomImagesTask, self).__init__(inputs, output, params)

    def run(self):
        pass