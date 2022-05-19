from app.models.helpers import CRUDMixin
from app.extensions import db


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    deleted = db.Column(db.DateTime, nullable=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, basestring) and record_id.isdigit(), isinstance(record_id, (int, float)),)):
            return cls.query.get(int(record_id))
        return None

    @classmethod
    def get_list(cls):
        """Get the list of records without sofly deleted."""
        return cls.query.filter(cls.deleted.__eq__(None)).all()

    @classmethod
    def default_query(cls):
        """Return not deleted models."""
        return cls.query.filter(cls.deleted.is_(None))
