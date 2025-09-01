from abc import ABC, abstractmethod


class Data(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def object(self):
        pass

    @abstractmethod
    def set_object(self, object) -> None:
        pass