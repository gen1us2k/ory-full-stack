from app.extensions import db
from app.models.base import PkModel


class User(PkModel):
    __tablename__ = 'users'
    kratos_id = db.Column(db.String(36))
    email = db.Column(db.String())

    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    subreddits = db.relationship('SubReddit', backref='user', lazy='dynamic')

