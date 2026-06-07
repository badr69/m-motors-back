"""merge heads

Revision ID: 3eb8cee2dadb
Revises: 3232e30c43be, a8925f03b29d
Create Date: 2026-06-07 12:26:03.001932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eb8cee2dadb'
down_revision: Union[str, Sequence[str], None] = ('3232e30c43be', 'a8925f03b29d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
