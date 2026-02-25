import uuid
from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class TokenBlacklist(Base):
    """
        Token blacklist model representing tokens in the application.
    """

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    token: Mapped[str] = mapped_column(String, index=True, nullable=False)
    blacklisted_on = mapped_column(DateTime, default=func.now())
