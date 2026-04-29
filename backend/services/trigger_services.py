from services.news_services import get_relevant_news_for_user, filter_triggered_news
from services.interest_services import get_user_interests


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

    return triggered_articles