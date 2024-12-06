class StrategyLogic:
    def should_enter_trade(self, **kwargs):
        raise NotImplementedError

    def should_exit_trade(self, **kwargs):
        raise NotImplementedError