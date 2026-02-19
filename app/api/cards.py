from fastapi import APIRouter
from app.schemas.card import AddCardRequest, CardResponse, SkryfallCard
from app.services.collection import add_card, lookup_card
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
    breakpoint()
    return result


# @router.get("/search_by", response_model=SkryfallCard)
# def search_cards_endpoint(payload: AddCardRequest):
#     "Return cards according to a specific search parameter"
#     logger.info(f"Returning cards with {payload.parameter}")
#     logger.info(f"payload: {payload}")
#     result = lookup_card_by_parameter
    