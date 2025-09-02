from abc import ABC, abstractmethod


class Loader(ABC):

    @abstractmethod
    def load(self, to_manager=True):
        pass