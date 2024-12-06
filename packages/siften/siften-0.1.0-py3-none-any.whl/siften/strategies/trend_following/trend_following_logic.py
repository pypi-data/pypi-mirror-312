import logging

from ...common.services.strategy_logic import StrategyLogic

logger = logging.getLogger()


class TrendFollowingLogic(StrategyLogic):
    def should_enter_trade(self, short_ema, long_ema, transaction_cost, **kwargs):
        # Logic for entering a trade in trend following strategy
        enter_trade = short_ema > long_ema and transaction_cost <= kwargs['maximum_allowable_cost']
        logger.debug(f"Evaluated conditions for entering a trade - Short EMA: {short_ema:.8f}, Long EMA: {long_ema:.8f}, Transaction Cost: {transaction_cost:.8f}, Maximum Allowable Cost: {kwargs['maximum_allowable_cost']:.8f}")
        logger.debug(f"Should enter trade: {enter_trade}")
        return enter_trade

    def should_exit_trade(self, short_ema, long_ema, current_price, buy_price, transaction_cost, **kwargs):
        # Logic for exiting a trade in trend following strategy
        exit_trade = (
            (short_ema < long_ema or
             current_price >= (buy_price * kwargs['profit_take']) or
             current_price <= kwargs['highest_price'] * (1 - kwargs['trailing_stop']))
            and transaction_cost <= kwargs['maximum_allowable_cost']
        )
        logger.debug(f"Evaluated conditions for exiting a trade - Short EMA: {short_ema:.8f}, Long EMA: {long_ema:.8f}, Current Price: {current_price:.8f}, Buy Price: {buy_price:.8f}, Transaction Cost: {transaction_cost:.8f}, Maximum Allowable Cost: {kwargs['maximum_allowable_cost']:.8f}")
        logger.debug(f"Should exit trade: {exit_trade}")
        return exit_trade