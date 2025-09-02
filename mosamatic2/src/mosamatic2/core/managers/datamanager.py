import os
import json
import importlib

from mosamatic2.core.singleton import singleton
from mosamatic2.core.utils import create_name_with_timestamp, mosamatic_data_dir
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()


@singleton
class DataManager:
    def __init__(self):
        self._data = {}
        self._listeners = []

    def add(self, data):
        if not data.name():
            data.set_name(create_name_with_timestamp(f'{data.__class__.__name__.lower()}-'))
        if not data.name() in self._data.keys():
            self._data[data.name()] = data
            self.notify_listeners(self._data[data.name()])
        else:
            LOG.warning(f'Data object with name "{data.name()}" already added')
        return data.name()

    def remove(self, name):
        if name in self._data.keys():
            del self._data[name]

    def remove_all(self, include_saved=False):
        self._data.clear()
        if include_saved:
            os.remove(os.path.join(mosamatic_data_dir(), 'data.json'))
    
    def get(self, name):
        if name in self._data.keys():
            return self._data[name]
        return None
    
    def print(self, suppress_output=False):
        messages = []
        for k, v in self._data.items():
            m = f'{k} = {v}'
            messages.append(m)
            if not suppress_output:
                LOG.info(m)
        return messages
    
    def add_listener(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def notify_listeners(self, data):
        for listener in self._listeners:
            listener.new_data(data)

    def save_data_to_json(self):
        file_info = {}
        for data in self._data.values():
            file_info[data.name()] = {
                'class_name': data.__class__.__name__,
                'path': data.path(),
            }
        with open(os.path.join(mosamatic_data_dir(), 'data.json'), 'w') as f:
            json.dump(file_info, f, indent=4)

    def load_data_from_json(self):
        with open(os.path.join(mosamatic_data_dir(), 'data.json'), 'r') as f:
            file_info = json.load(f)
            for name, v in file_info.items():
                class_name = v['class_name']
                path = v['path']
                cls = self.load_class(class_name)
                data = cls()
                data.set_name(name)
                data.set_path(path)
                self.add(data)

    def load_class(self, class_name):
        class_full_name = f'mosamatic2.core.data.{class_name.lower()}.{class_name}'
        module_path, class_name = class_full_name.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls