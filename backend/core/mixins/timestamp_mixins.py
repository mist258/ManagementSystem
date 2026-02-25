from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column


class TimestampMixin:
    """
        Mixin class that adds timestamp column
        created_at, updated_at
    """
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
        index=True,
    )