from flask import Blueprint, request
from utils.response import success_response
from services.analytics_services import (
    get_news_stats,
    get_user_insights,
    get_news_trends
)
from models.dynamodb import DynamoDBClient   # NEW

analytics_bp = Blueprint("analytics", __name__)


#  Existing routes (KEEP THEM)

@analytics_bp.route("/analytics/news", methods=["GET"])
def news_analytics():
    return success_response(get_news_stats()), 200


@analytics_bp.route("/analytics/user/<user_id>", methods=["GET"])
def user_analytics(user_id):
    return success_response(get_user_insights(user_id)), 200


@analytics_bp.route("/analytics/trends", methods=["GET"])
def trends_analytics():
    return success_response(get_news_trends()), 200


# 🔥 NEW ROUTE FOR DASHBOARD GRAPH

@analytics_bp.route("/api/analytics", methods=["GET"])
def analytics_dashboard():
    try:
        db = DynamoDBClient()
        table = db.get_table("news_items")

        response = table.scan()
        items = response.get("Items", [])

        category_count = {}

        for item in items:
            cat = item.get("category", "General")
            category_count[cat] = category_count.get(cat, 0) + 1

        return {
            "status": "success",
            "data": {
                "category_distribution": category_count,
                "total_news": len(items)
            }
        }

    except Exception as e:
        print("ANALYTICS ERROR:", str(e))
        return {
            "status": "error",
            "message": str(e)
        }, 500