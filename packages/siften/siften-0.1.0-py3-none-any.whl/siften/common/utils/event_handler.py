class EventHandler:
    @staticmethod
    def get_time_left(event):
        """
        Get the time left from the event.

        :param event: AWS Lambda event data. It may include 'timeLeft' or be nested within 'lambdaOutput'.
        :return: The time left or None if not provided.
        """
        if "lambdaOutput" in event and "timeLeft" in event["lambdaOutput"]:
            return event["lambdaOutput"]["timeLeft"]
        else:
            return event.get("timeLeft")

    @staticmethod
    def update_time_left(time_left):
        """
        Update the time left. If time_left is None, use the default runtime.

        :param time_left: The current time left.
        :return: The updated time left.
        """
        if time_left is None:
            time_left = EventHandler.get_default_runtime()
        return max(time_left - 10, 0)

    @staticmethod
    def get_user_id(event):
        """
        Get the user ID from the event.

        :param event: AWS Lambda event data. It may include 'userId' or be nested within 'lambdaOutput'.
        :return: The user ID.
        """
        if "lambdaOutput" in event and "userId" in event["lambdaOutput"]:
            return event["lambdaOutput"]["userId"]
        else:
            return event.get("userId")

    @staticmethod
    def get_agent_id(event):
        """
        Get the agent ID from the event.

        :param event: AWS Lambda event data. It may include 'agentId' or be nested within 'lambdaOutput'.
        :return: The agent ID.
        """
        if "lambdaOutput" in event and "agentId" in event["lambdaOutput"]:
            return event["lambdaOutput"]["agentId"]
        else:
            return event.get("agentId")

    @staticmethod
    def get_symbol(event):
        """
        Get the symbol from the event.

        :param event: AWS Lambda event data. It may include 'symbol' or be nested within 'lambdaOutput'.
        :return: The symbol.
        """
        if "lambdaOutput" in event and "symbol" in event["lambdaOutput"]:
            return event["lambdaOutput"]["symbol"]
        else:
            return event.get("symbol")

    @staticmethod
    def get_quantity(event):
        """
        Get the quantity from the event.

        :param event: AWS Lambda event data. It may include 'quantity' or be nested within 'lambdaOutput'.
        :return: The quantity.
        """
        if "lambdaOutput" in event and "quantity" in event["lambdaOutput"]:
            return event["lambdaOutput"]["quantity"]
        else:
            return event.get("quantity")

    @staticmethod
    def get_exchange(event):
        """
        Get the exchange from the event.

        :param event: AWS Lambda event data. It may include 'exchange' or be nested within 'lambdaOutput'.
        :return: The exchange.
        """
        if "lambdaOutput" in event and "exchange" in event["lambdaOutput"]:
            return event["lambdaOutput"]["exchange"]
        else:
            return event.get("exchange")

    @staticmethod
    def get_strategy(event):
        """
        Get the strategy from the event.

        :param event: AWS Lambda event data. It may include 'strategy' or be nested within 'lambdaOutput'.
        :return: The strategy.
        """
        if "lambdaOutput" in event and "strategy" in event["lambdaOutput"]:
            return event["lambdaOutput"]["strategy"]
        else:
            return event.get("strategy")

    @staticmethod
    def get_stop_loss(event):
        """
        Get the stop loss from the event.

        :param event: AWS Lambda event data. It may include 'stopLoss' or be nested within 'lambdaOutput'.
        :return: The stop loss as an integer, or None if not provided or not a valid integer.
        """
        stop_loss = None
        if "lambdaOutput" in event and "stopLoss" in event["lambdaOutput"]:
            stop_loss = event["lambdaOutput"]["stopLoss"]
        else:
            stop_loss = event.get("stopLoss")

        try:
            return int(stop_loss) if stop_loss is not None else None
        except ValueError:
            return None

    @staticmethod
    def get_profit_take(event):
        """
        Get the profit take from the event.

        :param event: AWS Lambda event data. It may include 'profitTake' or be nested within 'lambdaOutput'.
        :return: The profit take as an integer, or None if not provided or not a valid integer.
        """
        profit_take = None
        if "lambdaOutput" in event and "profitTake" in event["lambdaOutput"]:
            profit_take = event["lambdaOutput"]["profitTake"]
        else:
            profit_take = event.get("profitTake")

        try:
            return int(profit_take) if profit_take is not None else None
        except ValueError:
            return None

    @staticmethod
    def get_default_runtime():
        """
        Get the default runtime for indefinite execution.

        :return: A large number representing 'indefinite' runtime (e.g., 24 hours in minutes).
        """
        return 24 * 60  # 24 hours in minutes
