import boto3
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(".env.local")

# Create a client for AWS SSM
ssm = boto3.client("ssm")

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_binance_api_key():
    """
    Fetch the Binance API Key from AWS SSM.
    """
    try:
        # Get the Binance API Key from AWS SSM
        binance_api_key = ssm.get_parameter(Name="BINANCE_API_KEY", WithDecryption=True)
        # Return the value of the Binance API Key
        return binance_api_key["Parameter"]["Value"]
    except Exception as e:
        logger.error("Failed to get Binance API Key", e)
        raise e


def get_binance_secret_key():
    """
    Fetch the Binance Secret Key from AWS SSM.
    """
    try:
        # Get the Binance Secret Key from AWS SSM
        binance_secret_key = ssm.get_parameter(
            Name="BINANCE_SECRET_KEY", WithDecryption=True
        )
        # Return the value of the Binance Secret Key
        return binance_secret_key["Parameter"]["Value"]
    except Exception as e:
        logger.error("Failed to get Binance Secret Key", e)
        raise e


def get_binance_api_key_test():
    """
    Fetch the Binance API Key for testing from environment variables or AWS SSM.
    """
    try:
        # First try to get from environment variables
        env_key = os.getenv("BINANCE_API_KEY_TEST")
        if env_key:
            return env_key

        # Fall back to AWS SSM if not in environment
        binance_api_key = ssm.get_parameter(
            Name="BINANCE_API_KEY_TEST", WithDecryption=True
        )
        return binance_api_key["Parameter"]["Value"]
    except Exception as e:
        logger.error("Failed to get Binance API Key", e)
        raise e


def get_binance_secret_key_test():
    """
    Fetch the Binance Secret Key for testing from environment variables or AWS SSM.
    """
    try:
        # First try to get from environment variables
        env_key = os.getenv("BINANCE_SECRET_KEY_TEST")
        if env_key:
            return env_key

        # Fall back to AWS SSM if not in environment
        binance_secret_key = ssm.get_parameter(
            Name="BINANCE_SECRET_KEY_TEST", WithDecryption=True
        )
        return binance_secret_key["Parameter"]["Value"]
    except Exception as e:
        logger.error("Failed to get Binance Secret Key", e)
        raise e
