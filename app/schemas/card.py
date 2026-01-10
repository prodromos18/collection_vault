# Schemas are pydantic data contracts
# used for API request validation etc
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class SkryfallCard(BaseModel):
    id: Optional[UUID] = None
    scryfall_id: str
    name: str
    mana_cost: str
    type_line: str
    oracle_text: str
    image_url: str

class CollectionCard(BaseModel):
    id: Optional[UUID] = None
    scryfall_id: str  # foreign key to ScryfallCard
    collection_id: Optional[str] = None
    quantity: int

class AddCardRequest(BaseModel):
    name: str
    quantity: int = 1

class CardResponse(BaseModel):
    name: str
    type_line: str
    mana_cost: str
    message: Optional[str] = None
    error_message: Optional[str] = None