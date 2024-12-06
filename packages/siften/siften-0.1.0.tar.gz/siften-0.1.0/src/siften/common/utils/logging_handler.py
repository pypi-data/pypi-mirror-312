import logging
from datetime import datetime, timedelta

from ...common.services.database_handler import DatabaseHandler


class LoggingHandler:
    """
    Custom logging handler to manage logging actions and configurations.
    """

    def __init__(self):
        """
        Constructor for the LoggingHandler class.
        """
        self.configure_logging()
        self.logger = logging.getLogger()

    def log_action(self, action):
        """
        Log the given action in a custom formatted manner.

        :param action: Action string to be logged (e.g., "BUY", "SELL", etc.).
        """
        action = action.upper()  # Convert action to uppercase
        if action in ["BUY", "SELL", "STOP LOSS", "PROFIT TAKE", "ERROR"]:
            log_message = f"[{action.lower()}] Posting {action.lower()} order..."
            self.logger.info(log_message)
            log_data = {
                "LEVEL": "INFO",
                "LOG_STREAM_ID": "log_stream_123",
                "MESSAGE": log_message,
                "USER_ID": "2f87bc28-cb01-42ac-abe7-88bf05c440b7",
                "AGENT_ID": "agent-2538609834153483",
            }
            DatabaseHandler.add_entry_to_database("LOGS", None, log_data=log_data)

        border_left = ">" * 10
        border_right = "<" * 10
        message = f"{border_left} {action} {border_right}"

        self.logger.info(message)

    def configure_logging(self):
        """
        Configure the logging settings.
        """
        logger = logging.getLogger()

        # Remove all existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S BST"  # Added 'BST' to indicate the time zone
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            BSTFormatter(log_format, datefmt=datefmt)
        )  # Use BSTFormatter

        logger.setLevel(logging.INFO)
        logger.addHandler(console_handler)


class BSTFormatter(logging.Formatter):
    """
    Custom logging formatter to display time in BST (British Summer Time).
    """

    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        """
        Format the log record's timestamp to display in BST.

        :param record: The log record.
        :param datefmt: Date format string.
        :return: Formatted timestamp in BST.
        """
        ct = self.converter(record.created)
        ct = ct + timedelta(hours=1)  # Convert to BST by adding 1 hour
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = f"{t},{record.msecs:.0f}"
        return s
