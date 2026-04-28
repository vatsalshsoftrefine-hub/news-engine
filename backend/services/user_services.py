import uuid
from models.dynamodb import DynamoDBClient


db_client = DynamoDBClient()


def create_user(name, email):
    table = db_client.get_table("users")

    user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email
    }

    table.put_item(Item=user)

    return user


def get_all_users():
    table = db_client.get_table("users")

    response = table.scan()

    return response.get("Items", [])