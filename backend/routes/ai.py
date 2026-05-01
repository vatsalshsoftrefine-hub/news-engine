from flask import Blueprint, request
from utils.response import success_response, error_response
from services.ai_services import get_ai_news
from services.chat_services import get_user_chats


ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ai/search", methods=["POST"])
def ai_search():
    data = request.get_json()

    query = data.get("query")
    user_id = data.get("user_id")

    if not query:
        return error_response("Query is required"), 400

    results = get_ai_news(query, user_id)

    return success_response(results), 200

@ai_bp.route("/ai/history/<user_id>", methods=["GET"])
def chat_history(user_id):
    chats = get_user_chats(user_id)
    return success_response(chats), 200