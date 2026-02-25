from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer


class IdPkMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)