from abc import ABC, abstractmethod


class ExchangeAPI(ABC):
    """
    Abstract base class for exchange APIs.
    """
    def __init__(self, symbol):
        self.symbol = symbol

    @abstractmethod
    def get_order_status(self, order_id: str, wait_time=1, max_attempts=60):
        """
        Abstract method to check the status of an order.

        :param order_id: The order ID.
        :param wait_time: Time to wait between each check (default: 1 second).
        :param max_attempts: Maximum number of attempts to check order status.
        """
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: str):
        """
        Abstract method to get details of an order by its ID.

        :param order_id: The order ID.
        """
        pass

    @abstractmethod
    def get_last_order(self):
        """
        Abstract method to retrieve the most recent order.
        """
        pass

    @abstractmethod
    def cancel_last_order(self):
        """
        Abstract method to cancel the most recent order.
        """
        pass