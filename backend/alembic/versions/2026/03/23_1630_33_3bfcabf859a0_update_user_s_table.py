"""update user's table

Revision ID: 3bfcabf859a0
Revises: ecfef26c78dd
Create Date: 2026-03-23 16:30:33.475044

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

import sqlalchemy as sa

revision: str = "3bfcabf859a0"
down_revision: str | Sequence[str] | None = "ecfef26c78dd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("role", sa.String(length=10), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
