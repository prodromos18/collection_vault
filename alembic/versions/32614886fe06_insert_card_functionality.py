"""insert_card_functionality

Revision ID: 32614886fe06
Revises: f12073d80dbf
Create Date: 2025-12-27 21:19:23.204269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32614886fe06'
down_revision: Union[str, Sequence[str], None] = 'f12073d80dbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
