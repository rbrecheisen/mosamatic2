from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData

LOG = LogManager()


class Task:
    def __init__(self, inputs, params):
        self._inputs = inputs
        self._params = params
        # Check that the inputs have the right type
        for k, v in self._inputs.items():
            assert isinstance(v, Data)
            assert isinstance(v, FileData)

    def input(self, name):
        return self._inputs[name]
    
    def param(self, name):
        return self._params[name]
    
    def set_progress(self, step, nr_steps):
        LOG.info(f'[{self.__class__.__name__}] step {step} from {nr_steps}')
    
    def run(self):
        raise NotImplementedError()