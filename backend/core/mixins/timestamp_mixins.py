from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    """
        Mixin class that adds timestamp column
        created_at, updated_at
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
        index=True,
    )