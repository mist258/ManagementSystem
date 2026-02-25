from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr

from core.config import settings
from utils import camel_case_to_snake_case

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    id: Mapped[int] = Column(Integer, primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
