import logging
from app.services.scryfall import fetch_card_data_by_name
from app.db.repositories.collection_repo import add_to_collection_with_scryfall
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

def add_card(name: str, quantity:int):
    session = SessionLocal()
    scryfall_card = fetch_card_data_by_name(name)
    if not scryfall_card:
        logger.error(f"Card with name {name} does not exist in scryfall")
        return {
                "name": name,
                "type_line": "",
                "mana_cost": "",
                "message": None,
                "error_message": f"Card '{name}' not found"
            }

    add_to_collection_with_scryfall(session,scryfall_card.scryfall_id, scryfall_card,
                                    quantity)


    return {
        "name": scryfall_card.name,
        "type_line": scryfall_card.type_line,
        "mana_cost": scryfall_card.mana_cost,
        "message": f"Successfully added {quantity}x {scryfall_card.name}",
        "error_message": None
    }

    