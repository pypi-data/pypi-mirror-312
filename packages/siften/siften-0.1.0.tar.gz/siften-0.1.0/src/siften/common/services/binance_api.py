import boto3
import logging
import requests
import time
import hmac
import hashlib
import json

from ...common.services.exchange_api import ExchangeAPI
from ...common.utils.logging_handler import LoggingHandler
from ...common.services.database_handler import DatabaseHandler
from ...common.services.transaction_cost_model import TransactionCostModel

logger = logging.getLogger()
logging_handler = LoggingHandler()

ssm = boto3.client("ssm")


class BinanceAPI(ExchangeAPI):
    """
    A class for interacting with the Binance API.
    """

    def __init__(self, symbol, strategy):
        """
        Constructor for the BinanceAPI class.

        :param symbol: Trading pair symbol (e.g., "BTCUSDT").
        :param strategy: Trading strategy.
        """
        super().__init__(symbol)
        self.BASE_URL = "https://api.binance.com"
        self.api_key = BinanceAPI.get_binance_api_key()
        self.api_secret = BinanceAPI.get_binance_secret_key()
        self.headers = {"X-MBX-APIKEY": self.api_key}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.database_handler = DatabaseHandler()
        self.strategy = strategy
        self.transaction_cost_model = TransactionCostModel(
            maker_fee=0.001, taker_fee=0.001
        )

    @staticmethod
    def get_binance_api_key():
        """
        Retrieve the Binance API Key from AWS Systems Manager (SSM) Parameter Store.

        :return: Binance API Key as a string.
        :raises Exception: If there's an error retrieving the parameter.
        """
        try:
            binance_api_key = ssm.get_parameter(
                Name="BINANCE_API_KEY", WithDecryption=True
            )
            return binance_api_key["Parameter"]["Value"]
        except Exception as e:
            logger.error("Failed to get Binance API Key", e)
            raise e

    @staticmethod
    def get_binance_secret_key():
        """
        Retrieve the Binance Secret Key from AWS Systems Manager (SSM) Parameter Store.

        :return: Binance Secret Key as a string.
        :raises Exception: If there's an error retrieving the parameter.
        """
        try:
            binance_secret_key = ssm.get_parameter(
                Name="BINANCE_SECRET_KEY", WithDecryption=True
            )
            return binance_secret_key["Parameter"]["Value"]
        except Exception as e:
            logger.error("Failed to get Binance Secret Key", e)
            raise e

    def buy(self, quantity, price):
        self.buy(quantity, price)

    def sell(self, quantity, price, order_type="LIMIT"):
        self.sell(quantity, price, order_type)

    def get_order_status(self, order_id, wait_time=1, max_attempts=75):
        """
        Check if an order has been filled.

        :param order_id: The order ID.
        :param wait_time: Time to wait between each check (default: 1 second).
        :param max_attempts: Maximum number of attempts to check order status.
        :return: True if order is filled, False otherwise.
        """
        attempts = 0
        while attempts < max_attempts:
            logger.debug(f"Attempt: {attempts}")
            order_id_str = str(order_id)
            order = self.get_order_by_id(order_id_str)
            if order and order["status"] == "FILLED":
                return True
            time.sleep(wait_time)
            attempts += 1
        return False

    def get_order_by_id(self, order_id):
        """
        Get details of an order by its ID.

        :param order_id: The order ID.
        :return: Order details as a dictionary.
        """
        try:
            timestamp = int(time.time() * 1000)
            query_string = (
                f"symbol={self.symbol}&orderId={order_id}&timestamp={timestamp}"
            )
            signature = hmac.new(
                self.api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()
            params = {
                "symbol": self.symbol,
                "orderId": order_id,
                "timestamp": timestamp,
                "signature": signature,
            }
            response = self.session.get(f"{self.BASE_URL}/api/v3/order", params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("[get_order_by_id] Error getting order details")
            logger.error(e)
            return None

    def get_last_order(self):
        """
        Retrieve the most recent order that wasn't cancelled.

        :return: Most recent order details as a dictionary.
        """
        try:
            timestamp = int(time.time() * 1000)
            query_string = f"symbol={self.symbol}&timestamp={timestamp}"
            signature = hmac.new(
                self.api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()
            params = {
                "symbol": self.symbol,
                "timestamp": timestamp,
                "signature": signature,
            }
            response = self.session.get(
                f"{self.BASE_URL}/api/v3/allOrders", params=params
            )
            orders_json = response.json()

            if not orders_json:
                logger.info("No orders found.")
                return None

            # Find the most recent order that wasn't cancelled
            for order in reversed(orders_json):
                if order["status"] != "CANCELED":
                    logger.info(f"The last order was a " + order["side"] + " order.")
                    logger.debug(order)
                    return order

            # If we've reached here, all recent orders were cancelled
            logger.info("All recent orders were cancelled.")
            return None
        except requests.exceptions.RequestException as e:
            raise ValueError("Error getting last order:", e)

    def cancel_last_order(self):
        """
        Cancel the most recent order.

        :return: True if successful, otherwise raises an exception.
        """
        try:
            last_order_data = self.get_last_order()
            last_order_id = last_order_data["orderId"]

            timestamp = int(time.time() * 1000)
            query_string = (
                f"symbol={self.symbol}&orderId={last_order_id}&timestamp={timestamp}"
            )
            signature = hmac.new(
                self.api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()
            params = {
                "symbol": self.symbol,
                "orderId": last_order_id,
                "timestamp": timestamp,
                "signature": signature,
            }
            logger.info("Cancelling last order...")
            response = self.session.delete(
                f"{self.BASE_URL}/api/v3/order", params=params
            )
            logger.debug(response)
            return True
        except requests.exceptions.RequestException as e:
            raise ValueError("[cancel_last_order] Error cancelling last order:", e)

    def calculate_momentum(self, current_price, interval, limit):
        """
        Calculate the momentum of a trading pair.

        :param current_price: The current price of the trading pair.
        :param interval: The interval for the klines/candlesticks.
        :param limit: The number of klines/candlesticks to retrieve.
        :return: Momentum value.
        """

        klines_url = f"{self.BASE_URL}/api/v3/klines?symbol={self.symbol}&interval={interval}&limit={limit}"
        response = self.session.get(klines_url)
        response_json = response.json()
        closes = [float(entry[4]) for entry in response_json]
        ma = sum(closes) / len(closes)

        momentum = current_price / ma - 1

        return momentum

    def calculate_ema(self, current_price, interval, limit, period):
        """
        Calculate the Exponential Moving Average (EMA) of a trading pair.

        :param current_price: The current price of the trading pair.
        :param interval: The interval for the klines/candlesticks.
        :param limit: The number of klines/candlesticks to retrieve.
        :param period: The period for the EMA calculation.
        :return: EMA value.
        """
        klines_url = f"{self.BASE_URL}/api/v3/klines?symbol={self.symbol}&interval={interval}&limit={limit}"
        response = self.session.get(klines_url)
        response_json = response.json()

        # Get the closing prices.
        closes = [float(entry[4]) for entry in response_json]

        # Add current price to the closes list.
        closes.append(current_price)

        # Initialise EMA with the first close price.
        ema = closes[0]
        multiplier = 2 / (period + 1)

        # Calculate EMA.
        for price in closes[1:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def get_order_book(self, limit=5):
        """
        Retrieve the order book for the specified trading pair.

        :param limit: Number of levels to retrieve. Default is 5.
        :return: Order book containing bids and asks.
        """
        endpoint = "/api/v3/depth"
        url = f"{self.BASE_URL}{endpoint}?symbol={self.symbol}&limit={limit}"

        response = self.session.get(url)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve order book: {data.get('msg', '')}")

        return data

    def get_current_price(self, symbol: str, BASE_URL: str, headers: dict):
        """
        Retrieve the current price of a trading pair from the given exchange.

        :param symbol: Trading pair symbol (e.g., "BTCUSDT").
        :param BASE_URL: Base URL of the exchange's API endpoint.
        :param headers: Headers to be sent with the request.
        :return: Current price as a float, or None if there's an error.
        """
        try:
            response = requests.get(
                f"{BASE_URL}/api/v3/ticker/price",
                headers=headers,
                params={"symbol": symbol},
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting current price due to a request exception: {e}")
            return None

        try:
            data = response.json()
            return float(data["price"])
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Error parsing the response or extracting the price: {e}")
            return None

    def get_open_orders(self, symbol, api_secret, BASE_URL, headers):
        """
        Retrieve the number of open orders for a trading pair from the given exchange.

        :param symbol: Trading pair symbol (e.g., "BTCUSDT").
        :param api_secret: API secret key for signing the request.
        :param BASE_URL: Base URL of the exchange's API endpoint.
        :param headers: Headers to be sent with the request.
        :return: Number of open orders.
        :raises ValueError: If there's an error retrieving the orders.
        """
        try:
            timestamp = int(time.time() * 1000)
            query_string = f"symbol={symbol}&timestamp={timestamp}"
            signature = hmac.new(
                api_secret.encode(), query_string.encode(), hashlib.sha256
            ).hexdigest()
            response = requests.get(
                f"{BASE_URL}/api/v3/openOrders",
                headers=headers,
                params={
                    "symbol": symbol,
                    "timestamp": timestamp,
                    "signature": signature,
                },
            )
            response.raise_for_status()  # raise exception if the response has an error status code
            orders = response.json()
            return len(orders)
        except requests.exceptions.RequestException as e:
            raise ValueError("Error getting open orders:", e)

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
                logger.error("Error parsing JSON response.")
                return None, None

            logger.debug(response)
            logger.debug(data)

            exchange_fees = self.transaction_cost_model.calculate_exchange_fees(
                quantity, price, "LIMIT"
            )
            slippage_rate = 0.002  # Adjust this value based on market conditions
            slippage_cost = self.transaction_cost_model.calculate_slippage_cost(
                quantity, price, slippage_rate
            )
            total_cost = quantity * price + exchange_fees + slippage_cost
            logger.info(
                f"Calculated transaction costs for buy order - Exchange Fees: {exchange_fees:.8f}, Slippage Cost: {slippage_cost:.8f}, Total Cost: {total_cost:.8f}"
            )

            if not self.get_order_status(buy_order_json["orderId"]):
                logger.info(f"Order ID: {buy_order_json['orderId']}")

                # Dynamic Pricing: Re-evaluate the order book and adjust the buy price
                order_book = self.get_order_book()
                best_bid = float(order_book["bids"][0][0])
                adjusted_price = best_bid * 1.0001  # Adjusted buy price
                adjusted_price = round(adjusted_price, 2)

                self.cancel_last_order()  # Cancel the previous unfilled order
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
                logger.error(f"Error adding to database: {db_error}")

            logging_handler.log_action("buy")

            # Update with latest buy order
            self.latest_buy_order = buy_order_json
            self.buy_price = price

            return response, data
        except Exception as e:
            logger.error(f"Error placing buy order: {e}")
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
                logger.error("Error parsing JSON response.")
                return None, None

            exchange_fees = self.transaction_cost_model.calculate_exchange_fees(
                quantity, price, order_type
            )
            slippage_rate = 0.002  # Adjust this value based on market conditions
            slippage_cost = self.transaction_cost_model.calculate_slippage_cost(
                quantity, price, slippage_rate
            )
            total_cost = quantity * price + exchange_fees + slippage_cost
            logger.info(
                f"Calculated transaction costs for sell order - Exchange Fees: {exchange_fees:.8f}, Slippage Cost: {slippage_cost:.8f}, Total Cost: {total_cost:.8f}"
            )

            if not self.get_order_status(sell_order_json["orderId"]):
                # Dynamic Pricing: Re-evaluate the order book and adjust the sell price
                order_book = self.get_order_book()
                best_ask = float(order_book["asks"][0][0])
                adjusted_price = best_ask * 0.9999  # Adjusted sell price
                adjusted_price = round(adjusted_price, 2)

                self.cancel_last_order()  # Cancel the previous unfilled order
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
                logger.error(f"Error adding to database: {db_error}")

            logger.debug(response)
            logger.debug(data)

            logging_handler.log_action("sell")

            return response, data
        except Exception as e:
            logger.error(f"Error placing sell order: {e}")
            return None, None
