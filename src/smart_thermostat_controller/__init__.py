from flask import Flask
from .routing import bp

def create_app(testing=False) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"  # Use environment variables in production

    app.register_blueprint(bp)

    if not testing:
        from .hardware import init_hardware
        init_hardware()

    return app
