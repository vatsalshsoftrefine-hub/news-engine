import uuid
from models.dynamodb import DynamoDBClient

db_client = DynamoDBClient()
table = db_client.get_table("users")


def create_user(name, email, password):
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": password
    }

    table.put_item(Item=item)
    return item


def get_user_by_email(email):
    response = table.scan()
    items = response.get("Items", [])

    for user in items:
        if user.get("email") == email:
            return user

    return None

def get_all_users():
    table = db_client.get_table("users")

    response = table.scan()

    return response.get("Items", [])

def get_user(user_id):
    table = db_client.get_table("users")

    response = table.get_item(Key={"id": user_id})

    return response.get("Item", {})