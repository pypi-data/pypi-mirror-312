import logging

from ..strategies.strategy_facade import StrategyFacade
from ..common.services.database_handler import DatabaseHandler
from ..common.utils.event_handler import EventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    """
    AWS Lambda function handler to initiate the trend following strategy.
    :param event: AWS Lambda event data. It should include 'userId', 'agentId', 'symbol', 'quantity', and optionally 'timeLeft'.
    :param context: AWS Lambda context object.
    :return: Dictionary with updated 'timeLeft', 'agentId', 'userId', 'symbol', 'quantity', and a status message.
    """
    logger.info(f"Received event: {event}")

    # Extract necessary information from the event
    user_id = EventHandler.get_user_id(event)
    agent_id = EventHandler.get_agent_id(event)
    time_left = EventHandler.get_time_left(event)
    symbol = EventHandler.get_symbol(event)
    quantity = EventHandler.get_quantity(event)
    exchange = EventHandler.get_exchange(event)
    strategy = EventHandler.get_strategy(event)
    stop_loss = EventHandler.get_stop_loss(event)
    profit_take = EventHandler.get_profit_take(event)

    # Validate required parameters
    if not user_id:
        return {"error": "User Id is required"}
    if not agent_id:
        return {"error": "Agent Id is required"}
    if not symbol:
        return {"error": "Symbol is required"}
    if not quantity:
        return {"error": "Quantity is required"}
    if not exchange:
        return {"error": "Exchange is required"}
    if not strategy:
        return {"error": "Strategy is required"}
    if not stop_loss:
        return {"error": "Stop Loss is required"}
    if not profit_take:
        return {"error": "Profit Take is required"}

    # If timeLeft is not provided, it will be None, and update_time_left will use the default runtime

    # Add entry to database as soon as the lambda function starts running
    log_stream_data = {
        "NAME": f"Trend Following Strategy - Agent {agent_id}",
        "ORDER_STREAM_ID": context.aws_request_id,
        "USER_ID": user_id,
        "AGENT_ID": agent_id,
    }
    DatabaseHandler.add_entry_to_database(
        "LOG_STREAMS", None, log_stream_data=log_stream_data
    )

    strategy = StrategyFacade()
    strategy_response = strategy.start(event)

    # Update timeLeft value
    updated_time_left = EventHandler.update_time_left(time_left)

    return {
        "timeLeft": updated_time_left,
        "agentId": agent_id,
        "userId": user_id,
        "symbol": symbol,
        "quantity": quantity,
        "exchange": exchange,
        "strategy": strategy,
        "stopLoss": stop_loss,
        "profitTake": profit_take,
        "strategyOutput": strategy_response,
    }
