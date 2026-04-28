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