from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.data.data import Data
from mosamatic2.core.data.filedata import FileData

LOG = LogManager()


class Task:
    INPUTS = []
    PARAMS = []
    OUTPUT = 'output'

    def __init__(self, inputs, params):
        self._inputs = inputs
        self._params = params
        self._output = None
        # Check that the inputs have the right type
        for k, v in self._inputs.items():
            assert isinstance(v, Data)
            assert isinstance(v, FileData)
        # Check that input and param names match specification
        assert len(self._inputs.keys()) == len(self.__class__.INPUTS)
        for k in self._inputs.keys():
            assert k in self.__class__.INPUTS
        assert len(self._params.keys()) == len(self.__class__.PARAMS)
        for k in self._params.keys():
            assert k in self.__class__.PARAMS

    def input(self, name):
        return self._inputs[name]
    
    def param(self, name):
        return self._params[name]
    
    def output(self):
        return self._output
    
    def set_output(self, output):
        self._output = output
    
    def set_progress(self, step, nr_steps):
        LOG.info(f'[{self.__class__.__name__}] step {step} from {nr_steps}')
    
    def run(self):
        raise NotImplementedError()