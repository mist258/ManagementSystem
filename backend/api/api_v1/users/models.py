from core.models import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from core.mixins import IdPkMixin, TimestampMixin


class User(IdPkMixin, Base):
    """
        User model representing users in the application.
    """

    hashed_password = Column(String, nullable=False)
    email: Mapped[str] = Column(
        String(50),
        unique=True,
        nullable=False
    )
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)
    is_staff: Mapped[bool] = Column(Boolean, default=False)

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False
    )

class UserProfile(IdPkMixin, TimestampMixin, Base):
    """
        UserProfile model representing user's profile in the application.
    """

    first_name: Mapped[str] = Column(String(50))
    last_name: Mapped[str] = Column(String(50))

    user_id: Mapped[int] = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    user = relationship(
        "User",
         back_populates="profile"
    )