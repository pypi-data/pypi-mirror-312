from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    @abstractmethod
    def start(self):
        pass
