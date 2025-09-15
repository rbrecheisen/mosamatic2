class Visualization:
    INPUTS = []
    PARAMS = []

    def __init__(self, inputs, params):
        self._inputs = inputs
        self._params = params
        # Check that the inputs match specification and type
        assert isinstance(self._inputs, dict)
        assert len(self._inputs.keys()) == len(self.__class__.INPUTS)
        for k, v in self._inputs.items():
            assert k in self.__class__.INPUTS
            assert isinstance(v, str)
        # Check that param names match specification (if not None)
        if self._params:
            assert len(self._params.keys()) == len(self.__class__.PARAMS)
            for k in self._params.keys():
                assert k in self.__class__.PARAMS

    def input(self, name):
        return self._inputs[name]
    
    def param(self, name):
        return self._params[name]

    def run(self):
        raise NotImplementedError()