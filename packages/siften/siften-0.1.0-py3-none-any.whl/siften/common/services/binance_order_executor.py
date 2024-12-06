import logging
import requests
import json
import time
import hmac
import hashlib

from ...common.services.order_executor import OrderExecutor
from ...common.services.binance_api import BinanceAPI
from ...common.services.database_handler import DatabaseHandler
from ...common.utils.logging_handler import LoggingHandler

logger = logging.getLogger()
logging_handler = LoggingHandler()


class BinanceOrderExecutor(OrderExecutor):

    def __init__(self, symbol, strategy):
        self.exchange_api = BinanceAPI(symbol)
        self.database_handler = DatabaseHandler()
        self.symbol = symbol
        self.strategy = strategy
        self.position = None
        self.api_key = BinanceAPI.get_binance_api_key()
        self.api_secret = BinanceAPI.get_binance_secret_key()
        self.BASE_URL = "https://api.binance.com"
        self.BASE_URL_TESTNET = "https://testnet.binance.vision"
        self.headers = {"X-MBX-APIKEY": self.api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
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

    def buy(self, quantity, price):
        """
        Place a buy order on the exchange.

        :param quantity: Quantity to buy.
        :param price: Buy price.
        :return: Tuple containing response and data.
        """
        try:
            side = "BUY"
            timestamp = int(time.time() * 1000)
            query_string = f"symbol={self.symbol}&side={side}&type=LIMIT&timeInForce=GTC&quantity={quantity}&price={price}&timestamp={timestamp}"
            signature = hmac.new(
                self.api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()

            params = {
                "symbol": self.symbol,
                "side": side,
                "type": "LIMIT",
                "timeInForce": "GTC",
                "quantity": quantity,
                "price": price,
                "timestamp": timestamp,
                "signature": signature,
            }

            response = self.session.post(f"{self.BASE_URL}/api/v3/order", params=params)

            try:
                data = json.loads(response.content)
                buy_order_json = json.loads(response.content)
            except json.JSONDecodeError:
                logger.error("[buy] Error parsing JSON response.")
                return None, None

            logger.debug(response)
            logger.debug(data)

            if not self.exchange_api.get_order_status(buy_order_json["orderId"]):
                logger.info(f"Order ID: {buy_order_json['orderId']}")

                # Dynamic Pricing: Re-evaluate the order book and adjust the buy price
                order_book = self.exchange_api.get_order_book()
                best_bid = float(order_book["bids"][0][0])
                adjusted_price = best_bid * 1.0001  # Adjusted buy price
                adjusted_price = round(adjusted_price, 2)

                self.exchange_api.cancel_last_order()  # Cancel the previous unfilled order
                logger.error(
                    f"Buy order not filled, cancelling and adjusting the price to {adjusted_price}"
                )

                return self.buy(
                    quantity, adjusted_price
                )  # Recursive call with the adjusted price

            try:
                self.database_handler.add_entry_to_database(
                    "ORDERS",
                    self.symbol,
                    0,
                    quantity,
                    0,
                    buy_order_json,
                    "",
                    "",
                    self.strategy,
                )
            except Exception as db_error:
                logger.error(f"[buy] Error adding to database: {db_error}")

            logging_handler.log_action("buy")

            # Update with latest buy order
            self.latest_buy_order = buy_order_json
            self.buy_price = price

            return response, data
        except Exception as e:
            logger.error(f"[buy] Error placing buy order: {e}")
            return None, None

    def sell(self, quantity, price, order_type="LIMIT"):
        """
        Place a sell order on the exchange.

        :param quantity: Quantity to sell.
        :param price: Sell price.
        :param order_type: Type of the order, can be 'LIMIT' or 'MARKET'. Default is 'LIMIT'.
        :return: Tuple containing response and data.
        """
        try:
            side = "SELL"
            timestamp = int(time.time() * 1000)

            if order_type != "MARKET":
                query_string = f"symbol={self.symbol}&side={side}&type=LIMIT&timeInForce=GTC&quantity={quantity}&price={price}&timestamp={timestamp}"
            else:
                query_string = f"symbol={self.symbol}&side={side}&type={order_type}&quantity={quantity}&timestamp={timestamp}"

            signature = hmac.new(
                self.api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()

            if order_type == "MARKET":
                params = {
                    "symbol": self.symbol,
                    "side": side,
                    "type": order_type,
                    "quantity": quantity,
                    "timestamp": timestamp,
                    "signature": signature,
                }
            else:  # If it's a LIMIT order, add timeInForce and price to the parameters
                params = {
                    "symbol": self.symbol,
                    "side": side,
                    "type": "LIMIT",
                    "timeInForce": "GTC",
                    "quantity": quantity,
                    "price": price,
                    "timestamp": timestamp,
                    "signature": signature,
                }

            response = self.session.post(f"{self.BASE_URL}/api/v3/order", params=params)

            try:
                data = json.loads(response.content)
                sell_order_json = json.loads(response.content)
            except json.JSONDecodeError:
                logger.error("[sell] Error parsing JSON response.")
                return None, None

            if not self.exchange_api.get_order_status(sell_order_json["orderId"]):
                # Dynamic Pricing: Re-evaluate the order book and adjust the sell price
                order_book = self.exchange_api.get_order_book()
                best_ask = float(order_book["asks"][0][0])
                adjusted_price = best_ask * 0.9999  # Adjusted sell price
                adjusted_price = round(adjusted_price, 2)

                self.exchange_api.cancel_last_order()  # Cancel the previous unfilled order
                logger.error(
                    f"Sell order not filled, cancelling and adjusting price to {adjusted_price}"
                )

                return self.sell(
                    quantity, adjusted_price, order_type
                )  # Recursive call with the adjusted price

            try:
                self.database_handler.add_entry_to_database(
                    "ORDERS",
                    self.symbol,
                    0,
                    quantity,
                    0,
                    sell_order_json,
                    "",
                    "",
                    self.strategy,
                )
            except Exception as db_error:
                logger.error(f"[sell] Error adding to database: {db_error}")

            logger.debug(response)
            logger.debug(data)

            logging_handler.log_action("sell")

            return response, data
        except Exception as e:
            logger.error(f"[sell] Error placing sell order: {e}")
            return None, None
