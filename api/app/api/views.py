from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from app.api.resource import ThreadResource, ThreadList
from app.api.schema import ThreadSchema
from app.extensions import apispec
from marshmallow import ValidationError


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(ThreadResource, "/threads/<int:thread_id>", endpoint="thread_by_id")
api.add_resource(ThreadList, "/threads", endpoint="threads")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("ThreadSchema", schema=ThreadSchema)
    apispec.spec.path(view=ThreadResource, app=current_app)
    apispec.spec.path(view=ThreadList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.
    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
