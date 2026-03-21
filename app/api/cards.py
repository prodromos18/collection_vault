from fastapi import APIRouter
from typing import List
from app.schemas.card import AddCardRequest, CardResponse, SearchRequest
from app.services.collection import add_card, lookup_card, lookup_card_by_parameters
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
