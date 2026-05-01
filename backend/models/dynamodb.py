import boto3
import os

class DynamoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DynamoDBClient, cls).__new__(cls)
            cls._instance.dynamodb = boto3.resource(
                "dynamodb",
                region_name="us-east-1",
                endpoint_url="http://dynamodb-local:8000",
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy"
            )
        return cls._instance

    def get_table(self, table_name):
        return self.dynamodb.Table(table_name)