from flask import Blueprint, request
from utils.response import success_response, error_response
from services.user_services import create_user, get_all_users

# Define blueprint
user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    # Basic validation
    if not data or not data.get("name") or not data.get("email"):
        return error_response("Name and email required"), 400

    user = create_user(data["name"], data["email"])

    return success_response(user, "User created"), 201


@user_bp.route("/users", methods=["GET"])
def fetch_users():
    users = get_all_users()

    return success_response(users), 200