class PositionManagementFacade:
    def check_condition(self, condition_type, **kwargs):
        if condition_type == 'enter_trade':
            return self._should_enter_trade(**kwargs)
        elif condition_type == 'exit_trade':
            return self._should_exit_trade(**kwargs)
        else:
            raise ValueError(f"Unknown condition type: {condition_type}")

    def _should_enter_trade(self, position, unfilled_orders):
        if position is not None:
            return False
        return unfilled_orders == 0

    def _should_exit_trade(self, position):
        return position == "long"