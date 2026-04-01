"""Flask app factory for the billing parser."""

from flask import Flask

from app.config import Config


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
