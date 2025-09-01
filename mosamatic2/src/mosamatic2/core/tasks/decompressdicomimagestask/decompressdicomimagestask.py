import os
import shutil
from mosamatic2.core.tasks.task import Task


class DecompressDicomImagesTask(Task):
    def __init__(self, inputs, output, params):
        super(DecompressDicomImagesTask, self).__init__(inputs, output, params)

    def run(self):
        pass