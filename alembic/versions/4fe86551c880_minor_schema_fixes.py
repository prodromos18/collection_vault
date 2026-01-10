"""minor_schema_fixes

Revision ID: 4fe86551c880
Revises: 59dc7d7dff66
Create Date: 2026-01-10 23:54:35.237722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fe86551c880'
down_revision: Union[str, Sequence[str], None] = '59dc7d7dff66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
