# Schemas are pydantic data contracts
# used for API request validation etc
from uuid import UUID
from pydantic import BaseModel

class SkryfallCard(BaseModel):
    id: UUID
    scryfall_id: str
    deck_id: str
    name: str
    mana_cost: float
    type_line: str
    oracle_text: str
    image_url: str

class CollectionCard(BaseModel):
    id: UUID
    scryfall_id: str # foreign key to ScryfallCard
    collection_id: str
    quantity: int

class AddCardRequest(BaseModel):
    name: str
    quantity: int

class CardResponse(BaseModel):
    type_line: str
    error_message: str