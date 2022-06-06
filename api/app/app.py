import string
import random

from flask import Flask, session
from flask_oauthlib.client import OAuth

from app.extensions import db, migrate, apispec
from app.auth.middleware import IntrospectionMiddleware
from config import settings
from app import api


def create_app(testing=False):
    """Application factory, used to create application."""
    app = Flask(__name__)
    app.config.from_object("config.settings")
    if testing:
        app.config["TESTING"] = True

    if settings.HYDRA_ADMIN_URL:
        app.wsgi_app = IntrospectionMiddleware(app.wsgi_app)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    set_context_processor(app)
    configure_oauth2(app)

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


def set_context_processor(app):
    """Set context processor for app."""

    def generate_state(self):
        alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase
        return ''.join(random.choice(alphabet) for i in range(32))

    @app.context_processor
    def set_email_session():
        state = self.generate_state()
        session['oauth2_state'] = state

        return {
            "oauth2_state": session.get("oauth2_state"),
        }


def configure_oauth2(app):
    oauth = OAuth()
    twitter = oauth.remote_app(
        'hydra',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        app_key='HYDRA'
    )
    oauth.init_app(app)
