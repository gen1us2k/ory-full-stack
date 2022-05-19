from app.extensions import db
from app.models.base import PkModel


class User(PkModel):
    __tablename__ = 'users'
    kratos_id = db.Column(db.String(36))
