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
    """
    Fetch chat history for user
    """

    table = db_client.get_table("chat_history")

    response = table.scan()
    items = response.get("Items", [])

    user_chats = [item for item in items if item.get("user_id") == user_id]

    # sort latest first
    user_chats.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return user_chats

print("DynamoDB endpoint:", db_client.dynamodb.meta.client.meta.endpoint_url)