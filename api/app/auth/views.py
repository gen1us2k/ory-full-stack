from flask import Blueprint, request


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/complete", methods=["GET"])
def complete():
    pass


