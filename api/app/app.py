from flask import Flask
from app.extensions import db

def create_app(testing=False):
    """Application factory, used to create application."""
    app = Flask(__name__)
    app.config.from_object("config.settings")
    if testing:
        app.config["TESTING"] = True

    configure_extensions(app)

    return app

def configure_extensions(app):
    """Configure flask extensions."""

    db.init_app(app)
