from flask import Blueprint, jsonify

# Blueprint for health routes
health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    Used to verify if the service is running
    """
    return jsonify({
        "status": "ok",
        "message": "News Engine is running"
    }), 200