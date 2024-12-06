class TimeHandler:
    @staticmethod
    def get_time_left(event):
        """
        Get the time left from the event.

        :param event: AWS Lambda event data. It may include 'timeLeft' or be nested within 'lambdaOutput'.
        :return: The time left.
        """
        if "lambdaOutput" in event and "timeLeft" in event["lambdaOutput"]:
            return event["lambdaOutput"]["timeLeft"]
        else:
            return event.get("timeLeft", 0)

    @staticmethod
    def update_time_left(time_left):
        """
        Update the time left.

        :param time_left: The current time left.
        :return: The updated time left.
        """
        return max(time_left - 10, 0)
