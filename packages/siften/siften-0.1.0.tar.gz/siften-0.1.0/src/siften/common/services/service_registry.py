import boto3
import logging

logger = logging.getLogger()

dynamodb = boto3.client("dynamodb")

# Service Registry Table Name
SERVICE_REGISTRY_TABLE = "SERVICE_REGISTRY"


class ServiceRegistry:
    def __init__(self, strategy, api_key, user_id):
        self.strategy = strategy
        self.api_key = api_key
        self.user_id = user_id
        self.service_id = f"{self.strategy}-{self.api_key}"

    def register_strategy(self):
        """
        Register the trading strategy in the service registry.
        """
        try:
            dynamodb.put_item(
                TableName=SERVICE_REGISTRY_TABLE,
                Item={
                    "SERVICE_ID": {"S": self.service_id},
                    "STRATEGY_NAME": {"S": self.strategy},
                    "INSTANCE_ID": {"S": self.api_key},
                    "USER_ID": {"S": self.user_id},
                    "STATUS": {"S": "RUNNING"},
                    "CONFIG": {"S": "DEFAULT"},
                },
            )
            logger.info(
                f"Registered strategy {self.strategy} with instance ID {self.api_key}"
            )
        except Exception as e:
            logger.error(f"Error registering strategy: {e}")

    def deregister_strategy(self):
        """
        Deregister the trading strategy from the service registry.
        """
        try:
            dynamodb.delete_item(
                TableName=SERVICE_REGISTRY_TABLE,
                Key={"SERVICE_ID": {"S": self.service_id}},
            )
            logger.info(
                f"Deregistered strategy {self.strategy} with instance ID {self.api_key}"
            )
        except Exception as e:
            logger.error(f"Error deregistering strategy: {e}")

    def poll_registry(self):
        """
        Poll the service registry for updates.
        """
        try:
            response = dynamodb.get_item(
                TableName=SERVICE_REGISTRY_TABLE,
                Key={"SERVICE_ID": {"S": self.service_id}},
            )
            if "Item" in response:
                status = response["Item"]["STATUS"]["S"]
                config = response["Item"]["CONFIG"]["S"]
                return status, config
            else:
                return None, None
        except Exception as e:
            logger.error(f"Error polling registry: {e}")
            return None, None
