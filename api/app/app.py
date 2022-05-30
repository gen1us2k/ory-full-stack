from flask import Flask
from app.extensions import db, migrate, apispec
from app.auth.middleware import AuthenticationMiddleware
from config import settings
from app import api


def create_app(testing=False):
    """Application factory, used to create application."""
    app = Flask(__name__)
    app.config.from_object("config.settings")
    if testing:
        app.config["TESTING"] = True

    if settings.KRATOS_API_URL:
        app.wsgi_app = AuthenticationMiddleware(app.wsgi_app)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)

    return app

def configure_extensions(app):
    """Configure flask extensions."""

    db.init_app(app)
    migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
