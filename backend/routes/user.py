from flask import Blueprint, request
from utils.response import success_response, error_response
from services.user_services import create_user, get_all_users

# Define blueprint
user_bp = Blueprint("user", __name__)

from flask import Blueprint, request
from utils.response import success_response, error_response
from services.user_services import create_user, get_user_by_email

user_bp = Blueprint("user", __name__)

@user_bp.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return error_response("Email and password required"), 400

    user = create_user(name, email, password)

    return success_response(user, "User created"), 201


@user_bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)

    if not user or user.get("password") != password:
        return error_response("Invalid credentials"), 401

    return success_response(user, "Login successful"), 200


@user_bp.route("/users", methods=["GET"])
def fetch_users():
    users = get_all_users()

    return success_response(users), 200