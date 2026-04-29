from services.news_services import get_relevant_news_for_user, filter_triggered_news
from services.interest_services import get_user_interests
import uuid
from datetime import datetime
from models.dynamodb import DynamoDBClient
from services.email_services import send_email
from services.user_services import get_user


db_client = DynamoDBClient()


def get_triggered_news(user_id):
    """
    Get high-priority news for user
    """

    user_data = get_user_interests(user_id)
    interests = user_data.get("interests", [])

    if not interests:
        return []

    # Step 1: Get relevant news
    relevant_articles = get_relevant_news_for_user(user_id, interests, limit=50)

    # Step 2: Filter triggered
    triggered_articles = filter_triggered_news(relevant_articles)


    # Save triggers
    save_triggers(user_id, triggered_articles)

    # Send email notification
    if triggered_articles:
        body = "\n\n".join([
            f"{a['title']}\n{a['link']}"
            for a in triggered_articles[:5]  # limit email size
        ])

        user = get_user(user_id)
        user_email = user.get("email")
        if user_email and triggered_articles:
             body = "\n\n".join([
                  f"{a['title']}\n{a['link']}"
                  for a in triggered_articles[:5]
                 ])
             
             send_email( 
                to_email=user_email,
                subject="🚨 News Alert!",
                body=body
                )

    return triggered_articles


def save_triggers(user_id, articles):
    """
    Save triggered news into DB
    """

    table = db_client.get_table("triggers")

    saved = []

    for article in articles:
       item = {
           "id": str(uuid.uuid4()),
           "user_id": user_id,
           "title": article.get("title"),
           "link": article.get("link"),
           "category": article.get("category"),  
           "relevance_score": article.get("relevance_score"),
           "created_at": datetime.utcnow().isoformat()
           }

    table.put_item(Item=item)
    saved.append(item)

    return saved
