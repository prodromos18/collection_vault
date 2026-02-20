"""enable_pg_trgm

Revision ID: 1caf19d29d90
Revises: 4fe86551c880
Create Date: 2026-02-20 10:56:37.043780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1caf19d29d90'
down_revision: Union[str, Sequence[str], None] = '4fe86551c880'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.create_index(
        "ix_skryfall_cards_name_trgm",
        "skryfall_cards",
        ["name"],
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_skryfall_cards_name_trgm",
        table_name="skryfall_cards",
    )
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
