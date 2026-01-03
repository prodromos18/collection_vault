import logging
from app.services.scryfall import fetch_card_data_by_name
from app.db.repositories.collection_repo import add_to_collection

logger = logging.getLogger(__name__)

def add_card(name: str, quantity:int):
    scryfall_card = fetch_card_data_by_name(name)

    if not scryfall_card:
        logger.error(f"Card with name {name} does not exist in scryfall")
    add_to_collection(card_id=scryfall_card.scryfall_id, quantity=quantity)
    return {
        "name": scryfall_card.name,
        "type_line": scryfall_card.type_line,
        "mana_cost": scryfall_card.mana_cost,
        "message": "Success",
        "error_message": None
    }
    