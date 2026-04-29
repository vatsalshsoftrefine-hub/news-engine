from models.dynamodb import DynamoDBClient
from collections import defaultdict

db_client = DynamoDBClient()


def get_news_stats():
    table = db_client.get_table("news_items")

    response = table.scan()
    items = response.get("Items", [])

    total_news = len(items)

    category_count = {}

    for item in items:
        category = item.get("category", "unknown")

        category_count[category] = category_count.get(category, 0) + 1

    return {
        "total_news": total_news,
        "category_distribution": category_count
    }

def get_user_insights(user_id):
    """
    Per-user analytics
    """

    table = db_client.get_table("triggers")

    response = table.scan()
    items = response.get("Items", [])

    # Filter user-specific triggers
    user_items = [item for item in items if item.get("user_id") == user_id]

    total_triggers = len(user_items)

    category_count = {}

    for item in user_items:
        category = item.get("category", "unknown")

        category_count[category] = category_count.get(category, 0) + 1

    return {
        "user_id": user_id,
        "total_triggers": total_triggers,
        "top_categories": category_count
    }

def get_news_trends():
    """
    Trend detection: news count per day
    """

    table = db_client.get_table("news_items")

    response = table.scan()
    items = response.get("Items", [])

    trends = defaultdict(int)

    for item in items:
        created_at = item.get("created_at", "")

        if created_at:
            date = created_at.split("T")[0]  # YYYY-MM-DD
            trends[date] += 1

    return dict(trends)