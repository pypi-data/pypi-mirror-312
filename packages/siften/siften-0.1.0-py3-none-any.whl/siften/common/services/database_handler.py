import logging
import boto3
import uuid
from decimal import Decimal, getcontext
from datetime import datetime, timedelta

logger = logging.getLogger()

# Set the precision for Decimal calculations
getcontext().prec = 4

# Initialise AWS DynamoDB resource
dynamodb = boto3.resource("dynamodb")


class DatabaseHandler:
    @staticmethod
    def add_entry_to_database(table_name, symbol, *args, **kwargs):
        try:
            DatabaseHandler.add_to_database(table_name, symbol, *args, **kwargs)
        except Exception as db_error:
            logger.error(f"Error adding to database: {db_error}")

    @staticmethod
    def add_to_database(
        table_name,
        symbol,
        pnl=None,
        quantity=None,
        elapsed_time=None,
        order=None,
        start_time=None,
        end_time=None,
        strategy_type=None,
        log_stream_data=None,
        log_data=None,
    ):
        try:
            if table_name == "CONTAINER_REGISTRY":
                DatabaseHandler.add_container_item(
                    table_name, elapsed_time, start_time, end_time, strategy_type
                )
            elif table_name == "ORDERS":
                DatabaseHandler.add_order_item(table_name, symbol, order)
            elif table_name == "ORDER_STREAMS":
                DatabaseHandler.add_order_stream_item(
                    table_name, symbol, pnl, quantity, strategy_type
                )
            elif table_name == "OPEN_POSITIONS":
                DatabaseHandler.add_open_position_item(table_name, symbol, order)
            elif table_name == "PNL":
                DatabaseHandler.add_pnl_item(table_name, symbol, pnl)
            elif table_name == "LOG_STREAMS" and log_stream_data:
                DatabaseHandler.add_log_stream_item(table_name, log_stream_data)
            elif table_name == "LOGS" and log_data:
                DatabaseHandler.add_log_item(table_name, log_data)
            else:
                logger.error(f"Unknown table name: {table_name}")
        except Exception as e:
            logger.error(f"Error adding item to {table_name} table: {str(e)}")

    @staticmethod
    def add_container_item(
        table_name, elapsed_time, start_time, end_time, strategy_type
    ):
        try:
            order_id = uuid.uuid4().hex
            execution_time_seconds = elapsed_time
            memory_mb = 256
            runtime = "Python 3.11"
            strategy = strategy_type
            gb_seconds = DatabaseHandler.calculate_gb_seconds(
                execution_time_seconds, memory_mb
            )
            rounded_gb_seconds = round(gb_seconds, 2)
            gb_seconds_decimal = Decimal(str(rounded_gb_seconds))
            item = {
                "CONTAINER_ID": order_id,
                "CONTAINER_NAME": strategy,
                "GB_SECONDS": gb_seconds_decimal,
                "MEMORY": memory_mb,
                "RUNTIME": runtime,
                "START_TIME": start_time,
                "END_TIME": end_time,
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to CONTAINER_REGISTRY table with CONTAINER_ID {order_id} GB_SECONDS {gb_seconds_decimal}."
            )
        except Exception as e:
            logger.error(f"Error adding item to CONTAINER_REGISTRY table: {e}")

    @staticmethod
    def add_order_item(table_name, symbol, order):
        try:
            order_id = uuid.uuid4().hex
            timestamp = datetime.utcnow()
            bst_timestamp = timestamp + timedelta(hours=1)
            bst_timestamp_str = bst_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "ID": order_id,
                "SYMBOL": symbol,
                "EXECUTED_QTY": order["executedQty"],
                "ORDER_ID": order["orderId"],
                "ORDER_LIST_ID": order["orderListId"],
                "ORIG_QTY": order["origQty"],
                "STATUS": order["status"],
                "PRICE": order["price"],
                "SIDE": order["side"],
                "TIME_IN_FORCE": order["timeInForce"],
                "TYPE": order["type"],
                "SELF_TRADE_PREVENTION_MODE": order["selfTradePreventionMode"],
                "TIMESTAMP": bst_timestamp_str,
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to ORDERS table with ID {order_id} and SYMBOL {symbol}."
            )
        except Exception as e:
            logger.error(f"Error adding item to ORDERS table: {e}")

    @staticmethod
    def add_open_position_item(table_name, symbol, order):
        try:
            order_id = uuid.uuid4().hex
            timestamp = datetime.utcnow()
            bst_timestamp = timestamp + timedelta(hours=1)
            bst_timestamp_str = bst_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "ID": order_id,
                "SYMBOL": symbol,
                "EXECUTED_QTY": order["executedQty"],
                "ORDER_ID": order["orderId"],
                "ORDER_LIST_ID": order["orderListId"],
                "ORIG_QTY": order["origQty"],
                "STATUS": order["status"],
                "PRICE": order["price"],
                "SIDE": order["side"],
                "TIME_IN_FORCE": order["timeInForce"],
                "TYPE": order["type"],
                "SELF_TRADE_PREVENTION_MODE": order["selfTradePreventionMode"],
                "TIMESTAMP": bst_timestamp_str,
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to OPEN_POSITIONS table with ID {order_id} and SYMBOL {symbol}."
            )
        except Exception as e:
            logger.error(f"Error adding item to OPEN_POSITIONS table: {e}")

    @staticmethod
    def add_order_stream_item(table_name, symbol, pnl, quantity, strategy_type):
        try:
            order_id = uuid.uuid4().hex
            quantity_decimal = Decimal(str(quantity))
            rounded_pnl = round(pnl, 2)
            pnl_decimal = Decimal(str(rounded_pnl))
            strategy = strategy_type
            timestamp = datetime.utcnow()
            bst_timestamp = timestamp + timedelta(hours=1)
            bst_timestamp_str = bst_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "ID": order_id,
                "SYMBOL": symbol,
                "QUANTITY": quantity_decimal,
                "PNL": pnl_decimal,
                "STRATEGY": strategy,
                "TIMESTAMP": bst_timestamp_str,
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to ORDER_STREAMS table with symbol {symbol} and timestamp {bst_timestamp_str}."
            )
        except Exception as e:
            logger.error(f"Error adding item to ORDER_STREAMS table: {e}")

    @staticmethod
    def add_pnl_item(table_name, symbol, pnl):
        try:
            order_id = uuid.uuid4().hex
            rounded_pnl = round(pnl, 2)
            pnl_decimal = Decimal(str(rounded_pnl))
            timestamp = datetime.utcnow()
            bst_timestamp = timestamp + timedelta(hours=1)
            bst_timestamp_str = bst_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "ID": order_id,
                "SYMBOL": symbol,
                "PNL": pnl_decimal,
                "TIMESTAMP": bst_timestamp_str,
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to PNL table with symbol {symbol} and timestamp {bst_timestamp_str}."
            )
        except Exception as e:
            logger.error(f"Error adding item to PNL table: {e}")

    @staticmethod
    def add_log_stream_item(table_name, log_stream_data):
        try:
            log_stream_id = uuid.uuid4().hex
            created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = created_at
            item = {
                "LOG_STREAM_ID": log_stream_id,
                "CREATED_AT": created_at,
                "NAME": log_stream_data.get("NAME"),
                "ORDER_STREAM_ID": log_stream_data.get("ORDER_STREAM_ID"),
                "UPDATED_AT": updated_at,
                "USER_ID": log_stream_data.get("USER_ID"),
                "AGENT_ID": log_stream_data.get("AGENT_ID"),
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(
                f"Added item to LOG_STREAMS table with LOG_STREAM_ID {log_stream_id}."
            )
        except Exception as e:
            logger.error(f"Error adding item to LOG_STREAMS table: {e}")

    @staticmethod
    def add_log_item(table_name, log_data):
        try:
            log_id = uuid.uuid4().hex
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            item = {
                "LOG_ID": log_id,
                "LEVEL": log_data.get("LEVEL"),
                "LOG_STREAM_ID": log_data.get("LOG_STREAM_ID"),
                "MESSAGE": log_data.get("MESSAGE"),
                "TIMESTAMP": timestamp,
                "USER_ID": log_data.get("USER_ID"),
                "AGENT_ID": log_data.get("AGENT_ID"),
            }
            table = dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            logger.debug(response)
            logger.info(f"Added item to LOGS table with LOG_ID {log_id}.")
        except Exception as e:
            logger.error(f"Error adding item to LOGS table: {e}")

    @staticmethod
    def calculate_gb_seconds(execution_time_seconds, memory_mb):
        try:
            memory_gb = memory_mb / 1024
            gb_seconds = memory_gb * execution_time_seconds
            return gb_seconds
        except Exception as e:
            logger.error(f"Error calculating gb-seconds: {e}")
