"""Timestamp mixin for models"""

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """Timestamp mixin for models"""

    @declared_attr
    def created_at(cls):  # pylint: disable=E0213
        """Represents time of creation in DB"""
        # pylint: disable=E1102
        return Column(
            DateTime(timezone=True),
            default=func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls):  # pylint: disable=E0213
        """Represents time of update in DB"""
        return Column(
            DateTime(timezone=True),
            default=func.now(),  # pylint: disable=E1102
            onupdate=func.now(),  # pylint: disable=E1102
            nullable=False,
        )
