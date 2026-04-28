from flask import Flask
from config.settings import Config
from utils.logger import setup_logger


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Setup logger
    logger = setup_logger()
    app.logger = logger

    logger.info("Application starting...")

    # Register routes
    from routes.health import health_bp
    app.register_blueprint(health_bp)

    from routes.user import user_bp
    app.register_blueprint(user_bp)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """
    Centralized error handling
    """

    @app.errorhandler(404)
    def not_found(error):
        return {
            "status": "error",
            "message": "Resource not found"
        }, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal Server Error: {error}")
        return {
            "status": "error",
            "message": "Internal server error"
        }, 500