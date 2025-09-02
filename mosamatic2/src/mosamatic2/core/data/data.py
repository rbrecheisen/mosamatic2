from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def set_name(self, name):
        pass