from flask import Flask
import logging
from config.settings import Config


def create_app():
    """
    Application Factory Function
    This creates and configures the Flask app instance
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Setup logging
    setup_logging(app)

    # Register routes (blueprints will come later)
    from routes.health import health_bp
    app.register_blueprint(health_bp)

    return app


def setup_logging(app):
    """
    Setup logging configuration for the application
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    app.logger.info("Logging is configured")