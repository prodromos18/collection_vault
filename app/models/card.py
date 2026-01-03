#models define how data is stored in the database
# Also, by appropriately setting up alembic env.py, we ensure
# that database migrations can be auto-generated based on these models.
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float, ForeignKey
from uuid import uuid4
from app.db.base import Base

class SkryfallCard(Base):
    __tablename__ = "skryfall_cards"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    scryfall_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    mana_cost = Column(Float, nullable=False)
    type_line = Column(String, nullable=False)
    oracle_text = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

class CollectionCard(Base):
    __tablename__ = "collection_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    scryfall_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skryfall_cards.id", ondelete="CASCADE"),
        nullable=False,
    )
    collection_id = Column(String, nullable=True)
    quantity = Column(Float, nullable=False, default=1)