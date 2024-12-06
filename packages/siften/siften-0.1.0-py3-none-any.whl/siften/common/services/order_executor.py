from abc import ABC, abstractmethod


class OrderExecutor(ABC):
    @abstractmethod
    def buy(self, quantity, price):
        pass

    @abstractmethod
    def sell(self, quantity, price, order_type='LIMIT'):
        pass
