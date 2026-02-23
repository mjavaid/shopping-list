"""create lists and items tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-23 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lists_id"), "lists", ["id"], unique=False)

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("list_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("checked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["list_id"], ["lists.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_items_id"), table_name="items")
    op.drop_table("items")
    op.drop_index(op.f("ix_lists_id"), table_name="lists")
    op.drop_table("lists")
