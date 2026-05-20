"""add document processing status

Revision ID: a9d2f4c7b8e1
Revises: 838074132a62
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a9d2f4c7b8e1"
down_revision: Union[str, Sequence[str], None] = "838074132a62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "documents",
        sa.Column(
            "status",
            sa.String(length=32),
            server_default="pending",
            nullable=False,
        ),
    )
    op.add_column(
        "documents",
        sa.Column("processing_error", sa.Text(), nullable=True),
    )
    op.add_column(
        "documents",
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        op.f("ix_documents_status"),
        "documents",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_documents_status"), table_name="documents")
    op.drop_column("documents", "processed_at")
    op.drop_column("documents", "processing_error")
    op.drop_column("documents", "status")
