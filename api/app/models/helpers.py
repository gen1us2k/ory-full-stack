from datetime import datetime

from app.extensions import db
from sqlalchemy import inspect
from sqlalchemy.orm.attributes import get_history


class SoftDeleteRecordModel:
    """Soft delete model."""

    deleted = db.Column(db.DateTime, nullable=True)


class CRUDMixin(SoftDeleteRecordModel):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self):
        """Save the record."""
        db.session.add(self)
        db.session.flush()
        return self

    def delete(self, commit=True):
        """Soft delete the record in the database."""
        self.deleted = datetime.utcnow()
        db.session.add(self)
        return commit and db.session.flush()

    def old_value(self, attr: str):
        """Get old value of the field."""
        hist = get_history(self, attr)
        return hist.deleted[0] if hist.added and hist.deleted else None

    def has_changed(self, *fields: str):
        """Check if params was changed."""
        state = inspect(self)
        return any(
            (state.get_history(field, True).has_changes() for field in fields)
            if fields
            else (state.get_history(field.key, True).has_changes() for field in state.attrs)
        )
