from __future__ import annotations

from typing import TYPE_CHECKING

from core.mixins import IdPkMixin, TimestampMixin
from core.models import Base

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from api.users.models import UserProfile


class Article(IdPkMixin, TimestampMixin, Base):
    """
        Article model representing tokens in the application.
    """

    title: Mapped[str] = mapped_column(String(70), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="articles"
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        "user_profiles.id",
         ondelete="SET NULL"
    ),
        nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1) # field for optimistic locking

    # SQLAlchemy indicates that the model supports optimistic locking via this column
    # The version column will be automatically used by the ORM to check the row version on commit
    __mapper_args__ = {
        "version_id_col": version,
    }

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)

