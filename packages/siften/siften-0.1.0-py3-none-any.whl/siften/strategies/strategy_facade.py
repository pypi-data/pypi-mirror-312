import logging

from ..common.utils.logging_handler import LoggingHandler
from ..common.services.binance_api import BinanceAPI
from ..strategies.trend_following.trend_following import TrendFollowingStrategy


class StrategyFacade:
    """
    A facade class to handle different trading strategies.

    Attributes:
        logging_handler (LoggingHandler): The logging handler for this facade.
        logger (Logger): Logger for logging messages.
        strategies (dict): A mapping of strategy names to their corresponding classes.
    """

    def __init__(self):
        """Initialises the StrategyFacade with default logging and strategies."""
        try:
            self.logging_handler = LoggingHandler()
            self.logging_handler.configure_logging()
        except Exception as e:
            raise RuntimeError(f"Failed to configure logging: {e}")

        self.logger = logging.getLogger()

        self.strategies = {
            "Trend Following": TrendFollowingStrategy,
        }

        self.exchanges = {"Binance": BinanceAPI}

    def start(self, event=None):
        """
        Starts a trading strategy based on the provided event.

        Args:
            event (dict, optional): The event containing details for the strategy.
                                    Defaults to None.

        Returns:
            dict: A dictionary with the status code and body of the response.

        The event dictionary can contain 'symbol', 'quantity', 'strategy', 'mu', 'sigma', 'r', 'T', and 'dt' keys.
        If these keys are not present, default values are used.
        """
        try:
            # Set default values
            symbol = "FLOKIUSDT"
            quantity_str = "100000"
            strategy_name = "Trend Following"
            exchange_name = "Binance"
            user_id = "2f87bc28-cb01-42ac-abe7-88bf05c440b7"
            mu = 0.1
            sigma = 0.2
            r = 0.05
            T = 1.0
            dt = 0.01
            maximum_allowable_cost = 100  # Default value for maximum allowable cost

            if event is not None:
                symbol = event.get("symbol", symbol)
                quantity_str = event.get("quantity", quantity_str)
                strategy_name = event.get("strategy", strategy_name)
                exchange_name = event.get("exchange", exchange_name)
                user_id = event.get("user_id", user_id)

                mu = event.get("mu", mu)
                sigma = event.get("sigma", sigma)
                r = event.get("r", r)
                T = event.get("T", T)
                dt = event.get("dt", dt)
                maximum_allowable_cost = event.get(
                    "maximum_allowable_cost", maximum_allowable_cost
                )

            try:
                quantity = float(quantity_str)
            except ValueError:
                raise ValueError("Invalid quantity format.")

            self.logger.info(
                f"Initiating {strategy_name} Strategy for {symbol} with quantity {quantity} on {exchange_name}"
            )

            strategy_class = self.strategies.get(strategy_name)
            if not strategy_class:
                raise ValueError(f"Strategy '{strategy_name}' not recognised")

            exchange_class = self.exchanges.get(exchange_name)
            if not exchange_class:
                raise ValueError(f"Exchange '{exchange_name}' not recognised")

            exchange_api = exchange_class(symbol, strategy_name)
            if strategy_name == "Optimal Stopping":
                strategy = strategy_class(
                    symbol, quantity, strategy_name, exchange_api, mu, sigma, r, T, dt
                )
            else:
                strategy = strategy_class(
                    symbol,
                    quantity,
                    strategy_name,
                    exchange_api,
                    maximum_allowable_cost,
                    user_id,
                )
            strategy.start()

            return {"statusCode": 200, "body": {"status": "success"}}
        except ValueError as ve:
            self.logger.error(f"Validation error: {ve}")
            return {
                "statusCode": 400,
                "body": {"status": "failure", "message": str(ve)},
            }
        except Exception as e:
            self.logger.error(f"Error executing {strategy_name} strategy: {str(e)}")
            return {"statusCode": 500, "body": {"status": "failure", "message": str(e)}}
