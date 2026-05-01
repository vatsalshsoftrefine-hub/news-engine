from models.dynamodb import DynamoDBClient

from models.dynamodb import DynamoDBClient

db_client = DynamoDBClient()
dynamodb = db_client.dynamodb.meta.client


def create_users_table():
    db = DynamoDBClient().dynamodb

    existing_tables = db.meta.client.list_tables()["TableNames"]

    if "users" in existing_tables:
        print("Users table already exists")
        return

    table = db.create_table(
        TableName="users",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    print("Users table created")


def create_news_table():
    db = DynamoDBClient().dynamodb

    existing_tables = db.meta.client.list_tables()["TableNames"]

    if "news_items" in existing_tables:
        print("News table already exists")
        return

    table = db.create_table(
        TableName="news_items",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    print("News table created")

def create_interests_table():
    db = DynamoDBClient().dynamodb

    existing_tables = db.meta.client.list_tables()["TableNames"]

    if "interests" in existing_tables:
        print("Interests table already exists")
        return

    table = db.create_table(
        TableName="interests",
        KeySchema=[
            {"AttributeName": "user_id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    print("Interests table created")


def create_triggers_table():
    db = DynamoDBClient().dynamodb

    existing_tables = db.meta.client.list_tables()["TableNames"]

    if "triggers" in existing_tables:
        print("Triggers table already exists")
        return

    table = db.create_table(
        TableName="triggers",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()
    print("Triggers table created")

def create_chat_history_table():
    table_name = "chat_history"

    print("Creating chat_history table...")   # ADD THIS

    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "chat_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "chat_id", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user_id-index",
                    "KeySchema": [
                        {"AttributeName": "user_id", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print("✅ chat_history table created")

    except Exception as e:
        print("⚠️ Chat table issue:", str(e))

print("DynamoDB endpoint:", db_client.dynamodb.meta.client.meta.endpoint_url)