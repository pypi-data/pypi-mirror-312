import time
import requests
from datetime import datetime, timedelta
import logging

from ...common.services.technical_analysis_facade import TechnicalAnalysisFacade
from ...common.services.strategy_logic_facade import StrategyLogicFacade
from ...common.services.position_management_facade import PositionManagementFacade
from ...common.services.base_strategy import BaseStrategy
from ...common.services.binance_order_executor import logging_handler, logger
from ...common.services.binance_api import BinanceAPI
from ...common.services.database_handler import DatabaseHandler
from ...common.services.transaction_cost_model import TransactionCostModel
from ...common.services.service_registry import ServiceRegistry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TrendFollowingStrategy(BaseStrategy):
    """
    Defines a trend following trading strategy for the Binance exchange.
    """

    BASE_URL = "https://api.binance.com"
    BASE_URL_TESTNET = "https://testnet.binance.vision"
    PROFIT_TAKE_MULTIPLIER = 1.025
    STOP_LOSS_THRESHOLD = 0.025
    TIME_SLEEP_SHORT = 0.1
    TIME_SLEEP_LONG = 3
    TIME_SLEEP_MID = 7
    MAX_ELAPSED_TIME_SHORT = 540
    MAX_ELAPSED_TIME_LONG = 600
    PROFIT_THRESHOLD = 0.1

    def __init__(
        self, symbol, quantity, strategy, exchange_api, maximum_allowable_cost, user_id
    ):
        """
        Initialise trend following strategy for a given trading symbol and quantity.

        :param symbol: Trading symbol (e.g., "BTCUSDT").
        :param quantity: Trading quantity.
        :param strategy: Trading strategy.
        :param exchange_api: Exchange API instance.
        :param maximum_allowable_cost: Maximum allowable transaction cost.
        """
        # API and Database Configuration
        self.exchange_api = exchange_api
        self.database_handler = DatabaseHandler()
        self.api_key = BinanceAPI.get_binance_api_key()
        self.api_secret = BinanceAPI.get_binance_secret_key()
        self.BASE_URL = "https://api.binance.com"
        self.BASE_URL_TESTNET = "https://testnet.binance.vision"

        # Trading Configuration
        self.symbol = symbol
        self.quantity = quantity
        self.strategy = strategy
        self.user_id = user_id
        self.position = None
        self.profit_take = TrendFollowingStrategy.PROFIT_TAKE_MULTIPLIER
        self.trailing_stop = TrendFollowingStrategy.STOP_LOSS_THRESHOLD
        self.buy_price = None
        self.sell_price = None
        self.elapsed_time = 0
        self.num_iterations = 0
        self.buy_count = 0
        self.sell_count = 0
        self.stop_loss_count = 0
        self.profit_take_count = 0
        self.profit = 0
        self.highest_price = None
        self.latest_buy_order = None
        self.maximum_allowable_cost = maximum_allowable_cost

        # Initialise facades
        self.technical_analysis = TechnicalAnalysisFacade(self.exchange_api)
        self.position_management = PositionManagementFacade()
        self.strategy_logic = StrategyLogicFacade()
        self.transaction_cost_model = TransactionCostModel(
            maker_fee=0.001, taker_fee=0.001
        )

        # Session Initialization with Headers
        self.headers = {"X-MBX-APIKEY": self.api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Initialise Service Registry
        self.service_registry = ServiceRegistry(
            self.strategy, self.api_key, self.user_id
        )

    def start(self):
        """
        Start the trading process using the trend following strategy.
        """
        try:
            # Get the current price of the symbol
            current_price = self.get_current_price()
            if current_price is None:
                return

            # Set initial values
            self.buy_price = current_price
            self.sell_price = current_price * self.profit_take
            self.elapsed_time = 0
            self.num_iterations = 0
            self.buy_count = 0
            self.sell_count = 0
            self.stop_loss_count = 0
            self.profit_take_count = 0
            self.profit = 0

            start_time = time.time()  # used to calculate elapsed time
            utc_start_time = datetime.utcnow()
            bst_start_time = utc_start_time + timedelta(hours=1)
            bst_start_time_str = bst_start_time.strftime("%Y-%m-%d %H:%M:%S")

            log_interval = 30  # seconds
            iterations_for_log_interval = int(log_interval / self.TIME_SLEEP_SHORT)

            # Checking the last order state
            self.check_last_order()

            poll_interval = 5  # seconds
            last_poll_time = time.time()

            # Register the strategy
            self.service_registry.register_strategy()

            while True:
                # Get the current price of the symbol
                current_price = self.get_current_price()
                if current_price is None:
                    return

                # Poll the registry for updates every poll_interval seconds
                if time.time() - last_poll_time >= poll_interval:
                    current_status, current_config = (
                        self.service_registry.poll_registry()
                    )
                    if current_status == "STOPPED":
                        logger.info("Stopping the strategy as per registry update")
                        break
                    last_poll_time = time.time()

                # Calculate the short and long EMAs
                short_ema, long_ema = self.get_emas(current_price)

                # Get the unfilled orders
                unfilled_orders = self.get_unfilled_orders()

                if self.position == "long":
                    # Update the highest price
                    self.highest_price = max(
                        self.highest_price if self.highest_price else self.buy_price,
                        current_price,
                    )

                self.elapsed_time = time.time() - start_time

                enter_trade_conditions = {
                    "position": self.position,
                    "unfilled_orders": unfilled_orders,
                }

                exchange_fees = self.transaction_cost_model.calculate_exchange_fees(
                    self.quantity, current_price, "LIMIT"
                )
                slippage_rate = 0  # Adjust this value based on market conditions
                slippage_cost = self.transaction_cost_model.calculate_slippage_cost(
                    self.quantity, current_price, slippage_rate
                )
                total_cost = (
                    self.quantity * current_price + exchange_fees + slippage_cost
                )

                enter_trade_logic = {
                    "short_ema": short_ema,
                    "long_ema": long_ema,
                    "transaction_cost": total_cost,
                    "maximum_allowable_cost": self.maximum_allowable_cost,
                }

                # Check conditions for entering a trade
                if self.position_management.check_condition(
                    "enter_trade", **enter_trade_conditions
                ) and self.strategy_logic.check_logic(
                    "Trend Following", "buy", **enter_trade_logic
                ):
                    self.position = "long"
                    logger.info(
                        f"Conditions met for entering a trade. Position changed to 'long'. Buying {self.quantity} {self.symbol} at price {current_price:.8f}"
                    )
                    logger.info(
                        f"Transaction costs for buy order - Exchange Fees: {exchange_fees:.8f}, Slippage Cost: {slippage_cost:.8f}, Total Cost: {total_cost:.8f}"
                    )
                    self.exchange_api.buy(self.quantity, current_price)
                    self.highest_price = current_price

                exit_trade_conditions = {
                    "position": self.position,
                }

                exit_trade_logic = {
                    "short_ema": short_ema,
                    "long_ema": long_ema,
                    "current_price": current_price,
                    "buy_price": self.buy_price,
                    "transaction_cost": total_cost,
                    "maximum_allowable_cost": self.maximum_allowable_cost,
                    "profit_take": self.profit_take,
                    "highest_price": self.highest_price,
                    "trailing_stop": self.trailing_stop,
                }

                # Check conditions for taking profit or triggering trailing stop
                if self.position_management.check_condition(
                    "exit_trade", **exit_trade_conditions
                ) and self.strategy_logic.check_logic(
                    "Trend Following", "sell", **exit_trade_logic
                ):
                    pnl = (current_price - self.buy_price) * self.quantity - total_cost
                    self.profit += pnl
                    logger.info(
                        f"Conditions met for exiting a trade. Selling {self.quantity} {self.symbol} at price {current_price:.8f}"
                    )
                    logger.info(
                        f"Transaction costs for sell order - Exchange Fees: {exchange_fees:.8f}, Slippage Cost: {slippage_cost:.8f}, Total Cost: {total_cost:.8f}"
                    )
                    logger.info(f"Realized PnL: {pnl:.8f}")
                    self.exchange_api.sell(self.quantity, current_price)
                    self.position = None
                    self.highest_price = None

                logger.debug(
                    f"Current Price: {current_price}, Short EMA: {short_ema}, Long EMA: {long_ema}"
                )

                self.num_iterations += 1
                if self.num_iterations % iterations_for_log_interval == 0:
                    self.log_strategy_info(current_price)

                # Check if the elapsed time has passed the maximum allowed time
                if self.check_elapsed_time(start_time, bst_start_time_str):
                    break

                time.sleep(self.TIME_SLEEP_SHORT)

        except Exception as e:
            logger.error(f"Error in the trading loop: {e}")

        finally:
            # Deregister the strategy in the Service Registry table
            self.service_registry.deregister_strategy()

    def get_current_price(self):
        """
        Get the current price of the symbol from the exchange API.

        :return: The current price.
        """
        try:
            current_price = self.exchange_api.get_current_price(
                self.symbol, self.BASE_URL, self.headers
            )
            return current_price
        except Exception as api_error:
            logger.error(f"Error fetching the current price: {api_error}")
            return None

    def check_last_order(self):
        """
        Check the last order and set the position and buy price accordingly.

        :return: None
        """
        last_order = self.get_last_order()
        if last_order is None:
            return

        if (
            last_order
            and last_order["side"] == "BUY"
            and self.exchange_api.get_order_status(last_order["orderId"])
        ):
            self.position = "long"
            self.buy_price = float(last_order["price"])
            logger.info(
                f"Resuming from last BUY order. Position set to 'long' with buy price: {self.buy_price}"
            )

    def get_last_order(self):
        """
        Get the last order from the exchange API.

        :return: The last order.
        """
        try:
            last_order = self.exchange_api.get_last_order()
            logger.info(f"Fetched last order: {last_order}")
            return last_order
        except Exception as api_error:
            logger.error(f"Error fetching the last order: {api_error}")
            return None

    def get_unfilled_orders(self):
        """
        Get the unfilled orders from the exchange API.

        :return: The unfilled orders.
        """
        unfilled_orders = self.exchange_api.get_open_orders(
            self.symbol, self.api_secret, self.BASE_URL, self.headers
        )
        logger.debug(f"Unfilled Orders: {unfilled_orders}")
        return unfilled_orders

    def update_database(self, bst_start_time_str, bst_timestamp_str):
        try:
            if self.latest_buy_order is not None:
                try:
                    print("Latest buy order: ", self.latest_buy_order)
                    self.database_handler.add_entry_to_database(
                        "OPEN_POSITIONS",
                        self.symbol,
                        0,
                        self.quantity,
                        0,
                        self.latest_buy_order,
                        "",
                        "",
                        self.strategy,
                    )
                except Exception as db_error:
                    logger.error(f"Error adding to database: {db_error}")

            self.database_handler.add_entry_to_database(
                "CONTAINER_REGISTRY",
                self.symbol,
                self.profit,
                self.quantity,
                self.elapsed_time,
                {},
                bst_start_time_str,
                bst_timestamp_str,
                self.strategy,
            )

            self.database_handler.add_entry_to_database(
                "ORDER_STREAMS",
                self.symbol,
                self.profit,
                self.quantity,
                self.elapsed_time,
                {},
                "",
                "",
                self.strategy,
            )

            self.database_handler.add_entry_to_database(
                "PNL",
                self.symbol,
                self.profit,
                self.quantity,
                self.elapsed_time,
                {},
                "",
                "",
                self.strategy,
            )

        except Exception as db_error:
            logger.error(f"Error adding to database: {db_error}")

    def get_emas(self, current_price):
        """
        Get the short and long EMAs.

        :param current_price: The current price of the symbol.
        :return: The short and long EMAs.
        """
        short_ema = self.technical_analysis.get_technical_indicator(
            "short_ema", current_price, self.symbol, "1m", 50, period=12
        )
        long_ema = self.technical_analysis.get_technical_indicator(
            "long_ema", current_price, self.symbol, "1m", 50, period=26
        )
        logger.debug(f"Short EMA: {short_ema}, Long EMA: {long_ema}")

        return short_ema, long_ema

    def check_elapsed_time(self, start_time, bst_start_time_str):
        """
        Check if the elapsed time has passed the maximum allowed time.

        :param start_time: The start time of the trading process.
        :param bst_start_time_str: The start time in BST timezone as a string.
        :return: A boolean indicating whether the elapsed time has passed the maximum allowed time.
        """
        self.elapsed_time = time.time() - start_time
        if self.elapsed_time > self.MAX_ELAPSED_TIME_LONG:
            timestamp = datetime.utcnow()
            bst_timestamp = timestamp + timedelta(hours=1)
            bst_timestamp_str = bst_timestamp.strftime("%Y-%m-%d %H:%M:%S")

            self.update_database(bst_start_time_str, bst_timestamp_str)

            logger.info(
                "The elapsed time is greater than the set maximum. Trading has been terminated..."
            )
            return True

        return False

    def log_strategy_info(self, current_price):
        """
        Log the strategy information.

        :param current_price: The current price of the symbol.
        """
        logger.info(f"Elapsed Time: {self.elapsed_time:.2f} seconds")
        logger.info(f"Current Position: {self.position}")
        logger.info(f"Current Price: {current_price}")
        logger.info(f"Highest Price (since last buy): {self.highest_price}")
        logger.info(
            f"Profit/Loss (since last buy): {(current_price - (self.buy_price or 0)) * self.quantity}"
        )
