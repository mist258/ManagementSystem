from core.models import Base
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.mixins import IdPkMixin, TimestampMixin


class User(IdPkMixin, Base):
    """
        User model representing users in the application
    """

    hashed_password = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) # "True" for all roles in system (if is_active=False -> soft deletion )
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False) # "True" only for superuser
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False) # "True" for editor and superuser

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, email={self.email!r})"

    def __repr__(self):
        return str(self)


class UserProfile(IdPkMixin, TimestampMixin, Base):
    """
        UserProfile model representing user's profile in the application
    """

    first_name: Mapped[str] = mapped_column(String(50), index=True)
    last_name: Mapped[str] = mapped_column(String(50), index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    user: Mapped["User"] = relationship(
        "User",
         back_populates="profile"
    )
    articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="author"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.first_name!r} {self.last_name!r}), )"

    def __repr__(self):
        return str(self)

