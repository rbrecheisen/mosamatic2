class DixonSeriesData:
    def __init__(self):
        self._dir_path = None
        self._name = None
        self._series = {'ip': None, 'op': None, 'water': None, 'fat': None}

    def path(self):
        return self._dir_path
    
    def set_path(self, path):
        self._dir_path = path

    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def ip(self):
        return self._series['ip']
    
    def op(self):
        return self._series['op']
    
    def water(self):
        return self._series['water']
    
    def fat(self):
        return self._series['fat']
    
    def load(self):
        pass