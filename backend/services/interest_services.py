from models.dynamodb import DynamoDBClient

db_client = DynamoDBClient()


def add_user_interests(user_id, interests):
    """
    Store user interests
    """

    table = db_client.get_table("interests")

    item = {
        "user_id": user_id,
        "interests": interests
    }

    table.put_item(Item=item)

    return item


def get_user_interests(user_id):
    """
    Fetch user interests
    """

    table = db_client.get_table("interests")

    response = table.get_item(Key={"user_id": user_id})

    return response.get("Item", {})