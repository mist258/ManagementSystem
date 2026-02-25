from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.mixins import TimestampMixin, IdPkMixin


class Article(IdPkMixin, TimestampMixin, Base):
    """
        Article model representing tokens in the application.
    """

    title: Mapped[str] = mapped_column(String(70), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)

