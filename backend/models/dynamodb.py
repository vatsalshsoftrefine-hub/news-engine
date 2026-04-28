import boto3
import os


class DynamoDBClient:
    """
    Handles connection to DynamoDB (local or AWS)
    """

    def __init__(self):
        self.endpoint = os.getenv("DYNAMODB_ENDPOINT")
        self.region = os.getenv("AWS_REGION")

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=self.region,
            endpoint_url=self.endpoint,  # Important for local
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)