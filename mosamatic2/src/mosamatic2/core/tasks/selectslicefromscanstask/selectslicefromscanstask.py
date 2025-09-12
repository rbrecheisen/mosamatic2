from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()


class SelectSliceFromScansTask(Task):
    INPUTS = ['scans']
    PARAMS = ['vertebra']

    def __init__(self, inputs, params, output, overwrite):
        super(SelectSliceFromScansTask, self).__init__(inputs, params, output, overwrite)

    def run(self):
        pass