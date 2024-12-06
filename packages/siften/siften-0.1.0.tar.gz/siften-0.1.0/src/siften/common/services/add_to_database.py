import boto3
import uuid
from decimal import Decimal, getcontext
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()

# Set the precision for Decimal calculations
getcontext().prec = 4

# Initialise AWS DynamoDB resource
dynamodb = boto3.resource('dynamodb')


# Add data to different DynamoDB tables
def add_to_database(table_name, symbol, pnl, quantity, elapsed_time, order, start_time, end_time, strategy_type):
    """
    Add data to different DynamoDB tables.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param pnl: Profit or loss value.
    :param quantity: Quantity of the asset.
    :param elapsed_time: Time taken for execution.
    :param order: Order details.
    :param start_time: Start time of the execution.
    :param end_time: End time of the execution.
    :param strategy_type: Type of strategy.
    """
    try:
        # Call the appropriate function depending on the table name
        if table_name == "CONTAINER_REGISTRY":
            add_container_item(table_name, elapsed_time, start_time, end_time, strategy_type)
        elif table_name == "ORDERS":
            add_order_item(table_name, symbol, order)
        elif table_name == "ORDER_STREAMS":
            add_order_stream_item(table_name, symbol, pnl, quantity, strategy_type)
        elif table_name == "OPEN_POSITIONS":
            add_open_position_item(table_name, symbol, order)
        elif table_name == "PNL":
            add_pnl_item(table_name, symbol, pnl)
        else:
            logger.error(f"Unknown table name: {table_name}")
    except Exception as e:
        logger.error(f"Error adding item to {table_name} table: {str(e)}")


# Add an item to the CONTAINER_REGISTRY table
def add_container_item(table_name, elapsed_time, start_time, end_time, strategy_type):
    """
    Add an item to the CONTAINER_REGISTRY table.

    :param table_name: Name of the DynamoDB table.
    :param elapsed_time: Time taken for execution.
    :param start_time: Start time of the execution.
    :param end_time: End time of the execution.
    """
    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Set constants
        execution_time_seconds = elapsed_time
        memory_mb = 256
        runtime = 'Python 3.11'
        strategy = strategy_type

        # Calculate GB-seconds for AWS Lambda billing
        gb_seconds = calculate_gb_seconds(execution_time_seconds, memory_mb)
        rounded_gb_seconds = round(gb_seconds, 2)
        gb_seconds_decimal = Decimal(str(rounded_gb_seconds))

        # Create an item
        item = {
            'CONTAINER_ID': order_id,
            'CONTAINER_NAME': strategy,
            'GB_SECONDS': gb_seconds_decimal,
            'MEMORY': memory_mb,
            'RUNTIME': runtime,
            'START_TIME': start_time,
            'END_TIME': end_time
        }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to CONTAINER_REGISTRY table with CONTAINER_ID {order_id} GB_SECONDS {gb_seconds_decimal}.")
    except Exception as e:
        logger.error(f"Error adding item to CONTAINER_REGISTRY table: {e}")


# Add an item to the ORDERS table
def add_order_item(table_name, symbol, order):
    """
    Add an item to the ORDERS table.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param order: Order details.
    """

    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Get the current time in UTC and convert it to BST
        timestamp = datetime.utcnow()
        bst_timestamp = timestamp + timedelta(hours=1)
        bst_timestamp_str = bst_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Create an item with attributes from the buy order
        item = {
            'ID': order_id,
            'SYMBOL': symbol,
            'EXECUTED_QTY': order['executedQty'],
            'ORDER_ID': order['orderId'],
            'ORDER_LIST_ID': order['orderListId'],
            'ORIG_QTY': order['origQty'],
            'STATUS': order['status'],
            'PRICE': order['price'],
            'SIDE': order['side'],
            'TIME_IN_FORCE': order['timeInForce'],
            'TYPE': order['type'],
            'SELF_TRADE_PREVENTION_MODE': order['selfTradePreventionMode'],
            'TIMESTAMP': bst_timestamp_str
        }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to ORDERS table with ID {order_id} and SYMBOL {symbol}.")
    except Exception as e:
        logger.error(f"Error adding item to ORDERS table: {e}")


# Add an item to the OPEN_POSITIONS table
def add_open_position_item(table_name, symbol, order):
    """
    Add an item to the OPEN_POSITIONS table.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param order: Order details.
    """
    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Get the current time in UTC and convert it to BST
        timestamp = datetime.utcnow()
        bst_timestamp = timestamp + timedelta(hours=1)
        bst_timestamp_str = bst_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Create an item with attributes from the buy order
        item = {
            'ID': order_id,
            'SYMBOL': symbol,
            'EXECUTED_QTY': order['executedQty'],
            'ORDER_ID': order['orderId'],
            'ORDER_LIST_ID': order['orderListId'],
            'ORIG_QTY': order['origQty'],
            'STATUS': order['status'],
            'PRICE': order['price'],
            'SIDE': order['side'],
            'TIME_IN_FORCE': order['timeInForce'],
            'TYPE': order['type'],
            'SELF_TRADE_PREVENTION_MODE': order['selfTradePreventionMode'],
            'TIMESTAMP': bst_timestamp_str
        }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to OPEN_POSITIONS table with ID {order_id} and SYMBOL {symbol}.")
    except Exception as e:
        logger.error(f"Error adding item to OPEN_POSITIONS table: {e}")


# Add an item to the ORDER_STREAMS table
def add_order_stream_item(table_name, symbol, pnl, quantity, strategy_type):
    """
    Add an item to the ORDER_STREAMS table.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param pnl: Profit or loss value.
    :param quantity: Quantity of the asset.
    :param strategy_type: Type of strategy.
    """
    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Set constants
        quantity_decimal = Decimal(str(quantity))
        rounded_pnl = round(pnl, 2)
        pnl_decimal = Decimal(str(rounded_pnl))
        strategy = strategy_type
        timestamp = datetime.utcnow()

        # Add an hour to the UTC time to convert it to BST
        bst_timestamp = timestamp + timedelta(hours=1)
        bst_timestamp_str = bst_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Create an item
        item = {
            'ID': order_id,
            'SYMBOL': symbol,
            'QUANTITY': quantity_decimal,
            'PNL': pnl_decimal,
            'STRATEGY': strategy,
            'TIMESTAMP': bst_timestamp_str
        }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to ORDER_STREAMS table with symbol {symbol} and timestamp {bst_timestamp_str}.")
    except Exception as e:
        logger.error(f"Error adding item to ORDER_STREAMS table: {e}")


def add_order_status_item(table_name, symbol, order, strategy_type):
    """
    Add an item to the ORDER_STATUS table.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param order: Order details.
    :param strategy_type: Type of strategy.
    """
    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Set constants
        strategy = strategy_type
        timestamp = datetime.utcnow()

        # Add an hour to the UTC time to convert it to BST
        bst_timestamp = timestamp + timedelta(hours=1)
        bst_timestamp_str = bst_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        if order['side'] == 'BUY':
            # Create a buy item
            item = {
                'ID': order_id,
                'SYMBOL': symbol,
                'STRATEGY': strategy,
                'BUY_STATUS': order['status'],
                'BUY_PRICE': order['price'],
                'BUY_ORDER_ID': order['orderId'],
                'BUY_TIMESTAMP': bst_timestamp_str,
                'STATUS': 'OPEN'
            }
        elif order['side'] == 'SELL':
            # Create a sell item
            item = {
                'ID': order_id,
                'SYMBOL': symbol,
                'STRATEGY': strategy,
                'SELL_STATUS': order['status'],
                'SELL_PRICE': order['price'],
                'SELL_ORDER_ID': order['orderId'],
                'SELL_TIMESTAMP': bst_timestamp_str,
                'STATUS': 'FILLED'
            }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to ORDER_STATUS table with orderId {order_id} and symbol {symbol}.")
    except Exception as e:
        logger.error(f"Error adding item to ORDER_STATUS table: {e}")


# Add an item to the PNL table
def add_pnl_item(table_name, symbol, pnl):
    """
    Add an item to the PNL table.

    :param table_name: Name of the DynamoDB table.
    :param symbol: Stock or asset symbol.
    :param pnl: Profit or loss value.
    """
    try:
        # Generate a unique order id
        order_id = uuid.uuid4().hex

        # Set constants
        rounded_pnl = round(pnl, 2)
        pnl_decimal = Decimal(str(rounded_pnl))
        timestamp = datetime.utcnow()

        # Add an hour to the UTC time to convert it to BST
        bst_timestamp = timestamp + timedelta(hours=1)
        bst_timestamp_str = bst_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Create an item
        item = {
            'ID': order_id,
            'SYMBOL': symbol,
            'PNL': pnl_decimal,
            'TIMESTAMP': bst_timestamp_str
        }

        # Add the item to the table
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)
        logger.info(response)

        logger.info(f"Added item to PNL table with symbol {symbol} and timestamp {bst_timestamp_str}.")
    except Exception as e:
        logger.error(f"Error adding item to PNL table: {e}")


def calculate_gb_seconds(execution_time_seconds, memory_mb):
    """
    Calculate the GB-seconds, a metric used for lambda function billing.

    :param execution_time_seconds: Time of execution in seconds.
    :param memory_mb: Memory used in megabytes.
    :return: GB-seconds value.
    :raises Exception: If there's an error in the calculation.
    """
    try:
        memory_gb = memory_mb / 1024
        gb_seconds = memory_gb * execution_time_seconds

        return gb_seconds
    except Exception as e:
        logger.error(f"Error calculating gb-seconds: {e}")
