import logging

logger = logging.getLogger()


class TransactionCostModel:
    def __init__(self, maker_fee, taker_fee):
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee

    def calculate_exchange_fees(self, quantity, price, order_type):
        if order_type == "LIMIT":
            fee = quantity * price * self.maker_fee
        else:
            fee = quantity * price * self.taker_fee
        logger.debug(
            f"Calculated exchange fees: {fee:.8f} for order type: {order_type}"
        )
        return fee

    def calculate_slippage_cost(self, quantity, price, slippage_rate):
        slippage_cost = quantity * price * slippage_rate
        logger.debug(
            f"Calculated slippage cost: {slippage_cost:.8f} with slippage rate: {slippage_rate}"
        )
        return slippage_cost
