"""
Core functionality of the Siften library.
"""

import logging
import os
from dotenv import load_dotenv

from src.siften.strategies.strategy_facade import StrategyFacade
from src.siften.common.services.database_handler import DatabaseHandler
from src.siften.common.utils.event_handler import EventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def execute_strategy(
    user_id: str,
    agent_id: str,
    symbol: str,
    quantity: float,
    exchange: str,
    strategy: str,
    stop_loss: float,
    profit_take: float,
    time_left: int = None,
    request_id: str = None,
) -> dict:
    """
    Execute a trading strategy with the given parameters.

    Args:
        user_id (str): User identifier
        agent_id (str): Agent identifier
        symbol (str): Trading pair symbol
        quantity (float): Trading quantity
        exchange (str): Exchange name
        strategy (str): Strategy name
        stop_loss (float): Stop loss percentage
        profit_take (float): Take profit percentage
        time_left (int, optional): Remaining execution time
        request_id (str, optional): Unique request identifier

    Returns:
        dict: Strategy execution results
    """
    event = {
        "userId": user_id,
        "agentId": agent_id,
        "symbol": symbol,
        "quantity": quantity,
        "exchange": exchange,
        "strategy": strategy,
        "stopLoss": stop_loss,
        "profitTake": profit_take,
        "timeLeft": time_left,
    }

    log_stream_data = {
        "NAME": f"Trend Following Strategy - Agent {agent_id}",
        "ORDER_STREAM_ID": request_id,
        "USER_ID": user_id,
        "AGENT_ID": agent_id,
    }
    DatabaseHandler.add_entry_to_database(
        "LOG_STREAMS", None, log_stream_data=log_stream_data
    )

    strategy_facade = StrategyFacade()
    strategy_response = strategy_facade.start(event)

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


if __name__ == "__main__":
    load_dotenv()

    response = execute_strategy(
        user_id=os.getenv("TEST_USER_ID"),
        agent_id=os.getenv("TEST_AGENT_ID"),
        symbol=os.getenv("TEST_SYMBOL"),
        quantity=float(os.getenv("TEST_QUANTITY")),
        exchange=os.getenv("TEST_EXCHANGE"),
        strategy=os.getenv("TEST_STRATEGY"),
        stop_loss=float(os.getenv("TEST_STOP_LOSS")),
        profit_take=float(os.getenv("TEST_PROFIT_TAKE")),
    )
    print(response)
