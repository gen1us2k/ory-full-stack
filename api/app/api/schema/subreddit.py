from app.models import SubReddit
from app.extensions import ma, db


class SubRedditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubReddit
        sqla_session = db.session
