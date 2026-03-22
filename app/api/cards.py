from fastapi import APIRouter, HTTPException
from typing import List, Optional, Union
from app.schemas.card import AddCardRequest, CardResponse, SearchRequest, CardMatch, DeleteCardResponse
from app.services.collection import add_card, lookup_card, lookup_card_by_parameters, search_cards_by_name, delete_card
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cards", tags=["cards"])

@router.post("/add", response_model=CardResponse)
def add_card_endpoint(payload: AddCardRequest):
    """Add a card to the collection"""
    logger.info("add_card_endpoint has started")
    logger.info(f"payload: {payload}")
    result = add_card(
        name=payload.name,
        quantity=payload.quantity
    )
    
    return result

@router.get("/get", response_model=CardResponse)
def fetch_card_endpoint(name):
    """Look up a card in the collection"""
    logger.info("fetch_card_endpoint has started")
    logger.info(f"Looking up {name} in the collection")
    result = lookup_card(name)
    return result


@router.post("/search_by", response_model=List[CardResponse])
def search_cards_endpoint(payload: SearchRequest):
    """Return cards matching the given search criteria"""
    logger.info(f"Searching cards with criteria: {payload.criteria}")
    criteria = {field: {"op": c.op, "value": c.value} for field, c in payload.criteria.items()}
    result = lookup_card_by_parameters(**criteria)
    return result

@router.delete("", response_model=Union[DeleteCardResponse, List[CardMatch]])
def delete_card_endpoint(
    name: Optional[str] = None,
    scryfall_id: Optional[str] = None,
    quantity: Optional[float] = None,
):
    """
    Delete a card from the collection.

    - Provide `name` for fuzzy search: returns a list of matches if multiple are found,
      or deletes directly if only one match exists.
    - Provide `scryfall_id` for an exact delete (use after picking from a fuzzy match list).
    - Optionally provide `quantity` to reduce the count rather than fully removing the card.
    """
    if not name and not scryfall_id:
        raise HTTPException(status_code=400, detail="Provide either 'name' or 'scryfall_id'")

    if name and not scryfall_id:
        logger.info(f"Fuzzy searching collection for '{name}'")
        matches = search_cards_by_name(name)
        if not matches:
            raise HTTPException(status_code=404, detail=f"No card matching '{name}' found in collection")
        if len(matches) > 1:
            logger.info(f"Multiple matches found for '{name}', returning list")
            return matches
        scryfall_id = matches[0]["scryfall_id"]

    logger.info(f"Deleting scryfall_id={scryfall_id} quantity={quantity}")
    result = delete_card(scryfall_id=scryfall_id, quantity=quantity)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Card with scryfall_id '{scryfall_id}' not found in collection")
    return result
