from ...strategies.trend_following.trend_following_logic import TrendFollowingLogic


class StrategyLogicFacade:
    def __init__(self):
        self.strategies = {
            'Trend Following': TrendFollowingLogic(),
            # Add other strategies here
        }

    def check_logic(self, strategy_type, logic_type, **kwargs):
        strategy_logic = self.strategies.get(strategy_type)
        if not strategy_logic:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

        if logic_type == 'buy':
            return strategy_logic.should_enter_trade(**kwargs)
        elif logic_type == 'sell':
            return strategy_logic.should_exit_trade(**kwargs)
        else:
            raise ValueError(f"Unknown logic type: {logic_type}")  