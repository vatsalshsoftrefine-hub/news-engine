from flask import Blueprint, request
from utils.response import success_response, error_response
from services.news_services import fetch_news_from_rss, save_articles, get_news
from services.interest_services import get_user_interests
from services.news_services import get_relevant_news_for_user
from services.trigger_services import get_triggered_news
from models.dynamodb import DynamoDBClient

news_bp = Blueprint("news", __name__)


@news_bp.route("/ingest", methods=["POST"])
def ingest_news():
    data = request.get_json()

    rss_url = data.get("rss_url")

    if not rss_url:
        return error_response("rss_url is required"), 400

    articles = fetch_news_from_rss(rss_url)

    if not articles:
        return error_response("Failed to fetch articles"), 500

    count = save_articles(articles)

    return success_response(
        {"articles_saved": count},
        "News ingested successfully"
    ), 200

@news_bp.route("/news", methods=["GET"])
def fetch_news():
    category = request.args.get("category")
    limit = request.args.get("limit", 10)

    try:
        limit = int(limit)
    except:
        limit = 10

    articles = get_news(category, limit)

    return success_response(articles), 200

@news_bp.route("/news/relevant/<user_id>", methods=["GET"])
def relevant_news(user_id):
    user_data = get_user_interests(user_id)

    interests = user_data.get("interests", [])

    if not interests:
        return error_response("No interests found for user"), 404

    articles = get_relevant_news_for_user(user_id, interests)

    return success_response(articles), 200

@news_bp.route("/news/trigger/<user_id>", methods=["GET"])
def trigger_news(user_id):
    articles = get_triggered_news(user_id)

    return success_response(articles), 200

@news_bp.route("/news/history/<user_id>", methods=["GET"])
def trigger_history(user_id):
    db = DynamoDBClient()
    table = db.get_table("triggers")

    response = table.scan()
    items = response.get("Items", [])

    # Filter user-specific history
    user_items = [item for item in items if item.get("user_id") == user_id]

    return success_response(user_items), 200