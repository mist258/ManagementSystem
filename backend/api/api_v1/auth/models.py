from sqlalchemy import Column

from core.models import Base


class TokenBlacklist(Base):

    id = Column(UU)