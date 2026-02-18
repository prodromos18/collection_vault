from fastapi import APIRouter
from app.schemas.card import AddCardRequest, CardResponse
from app.services.collection import add_card
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