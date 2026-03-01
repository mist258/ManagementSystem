"""create tables

Revision ID: ecfef26c78dd
Revises:
Create Date: 2026-02-28 19:50:34.535570

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ecfef26c78dd"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_staff", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_profiles_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_profiles")),
        sa.UniqueConstraint("user_id", name=op.f("uq_user_profiles_user_id")),
    )
    op.create_index(
        op.f("ix_user_profiles_first_name"),
        "user_profiles",
        ["first_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_profiles_last_name"),
        "user_profiles",
        ["last_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_profiles_updated_at"),
        "user_profiles",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=70), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user_profiles.id"],
            name=op.f("fk_articles_author_id_user_profiles"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_articles")),
    )
    op.create_index(
        op.f("ix_articles_title"), "articles", ["title"], unique=False
    )
    op.create_index(
        op.f("ix_articles_updated_at"),
        "articles",
        ["updated_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_articles_updated_at"), table_name="articles")
    op.drop_index(op.f("ix_articles_title"), table_name="articles")
    op.drop_table("articles")
    op.drop_index(
        op.f("ix_user_profiles_updated_at"), table_name="user_profiles"
    )
    op.drop_index(
        op.f("ix_user_profiles_last_name"), table_name="user_profiles"
    )
    op.drop_index(
        op.f("ix_user_profiles_first_name"), table_name="user_profiles"
    )
    op.drop_table("user_profiles")
    op.drop_table("users")
