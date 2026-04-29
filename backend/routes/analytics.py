from flask import Blueprint, request
from utils.response import success_response
from services.analytics_services import (
    get_news_stats,
    get_user_insights,
    get_news_trends
)

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics/news", methods=["GET"])
def news_analytics():
    return success_response(get_news_stats()), 200


@analytics_bp.route("/analytics/user/<user_id>", methods=["GET"])
def user_analytics(user_id):
    return success_response(get_user_insights(user_id)), 200


@analytics_bp.route("/analytics/trends", methods=["GET"])
def trends_analytics():
    return success_response(get_news_trends()), 200