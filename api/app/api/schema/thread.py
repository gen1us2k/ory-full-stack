from app.models import Thread, Comment
from app.extensions import ma, db


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        sqla_session = db.session


class ThreadSchema(ma.SQLAlchemyAutoSchema):
    comments = ma.Nested(CommentSchema, many=True)
    class Meta:
        model = Thread
        sqla_session = db.session
