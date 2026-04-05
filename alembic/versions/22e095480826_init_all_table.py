"""init all table

Revision ID: 22e095480826
Revises: f880236ec7c3
Create Date: 2026-04-05 11:37:29.029221

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '22e095480826'
down_revision: Union[str, Sequence[str], None] = 'f880236ec7c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
