from flask import Blueprint, request
from utils.response import success_response, error_response
from services.interest_services import add_user_interests, get_user_interests

interest_bp = Blueprint("interest", __name__)


@interest_bp.route("/interests", methods=["POST"])
def add_interests():
    data = request.get_json()

    user_id = data.get("user_id")
    interests = data.get("interests")

    if not user_id or not interests:
        return error_response("user_id and interests required"), 400

    result = add_user_interests(user_id, interests)

    return success_response(result, "Interests saved"), 201


@interest_bp.route("/interests/<user_id>", methods=["GET"])
def fetch_interests(user_id):
    result = get_user_interests(user_id)

    return success_response(result), 200