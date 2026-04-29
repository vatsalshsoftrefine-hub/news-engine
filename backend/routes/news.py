from flask import Blueprint, request
from utils.response import success_response, error_response
from services.news_services import fetch_news_from_rss, save_articles

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