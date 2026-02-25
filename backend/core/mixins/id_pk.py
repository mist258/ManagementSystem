from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer


class IdPkMixin:
    id: Mapped[int] = Column(Integer, primary_key=True)