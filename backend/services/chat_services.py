import uuid
from datetime import datetime
from models.dynamodb import DynamoDBClient

db_client = DynamoDBClient()


def save_chat(user_id, query, response):
    """
    Save chat interaction
    """

    table = db_client.get_table("chat_history")

    item = {
        "chat_id": str(uuid.uuid4()),
        "user_id": user_id,
        "query": query,
        "response": response,
        "created_at": datetime.utcnow().isoformat()
    }

    print("SAVING CHAT:", item)

    table.put_item(Item=item)

    return item


def get_user_chats(user_id):
    table = db_client.get_table("chat_history")

    response = table.query(
        IndexName="user_id-index",
        KeyConditionExpression="user_id = :uid",
        ExpressionAttributeValues={
            ":uid": user_id
        }
    )

    items = response.get("Items", [])

    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return items

print("DynamoDB endpoint:", db_client.dynamodb.meta.client.meta.endpoint_url)