from flask import Flask
from .routing import bp

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"  # Use environment variables in production

    app.register_blueprint(bp)

    return app
