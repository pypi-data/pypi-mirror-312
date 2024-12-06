class TechnicalAnalysisFacade:
    def __init__(self, exchange_api):
        self.exchange_api = exchange_api

    def get_technical_indicator(self, indicator_name, current_price, symbol, interval, limit, **kwargs):
        if indicator_name == 'short_ema':
            return self.calculate_ema(current_price, interval, limit, kwargs.get('period', 12))
        elif indicator_name == 'long_ema':
            return self.calculate_ema(current_price, interval, limit, kwargs.get('period', 26))
        # Add cases for other indicators as needed
        else:
            raise ValueError(f"Unknown indicator: {indicator_name}")

    def calculate_ema(self, current_price, interval, limit, period):
        return self.exchange_api.calculate_ema(current_price, interval, limit, period)
