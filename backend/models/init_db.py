from models.dynamodb import DynamoDBClient


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