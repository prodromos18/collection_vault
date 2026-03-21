import logging
from app.services.scryfall import fetch_card_data_by_name
from app.db.repositories.collection_repo import (
    add_to_collection_with_scryfall,
    lookup_card_in_db,
    lookup_card_in_db_by_param
)
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

def lookup_card(name: str):
    session = SessionLocal()
    scryfall_card = lookup_card_in_db(session, name)
    if scryfall_card:
        return {
            "name": scryfall_card.name,
            "type_line": scryfall_card.type_line,
            "mana_cost": scryfall_card.mana_cost,
            "message": f"Successfully found {scryfall_card.name} in the collection",
            "error_message": None
        }

def lookup_card_by_parameters(**kwargs):
    session = SessionLocal()
    scryfall_cards = lookup_card_in_db_by_param(session, **kwargs)
    return [
        {
            "name": card.name,
            "type_line": card.type_line,
            "mana_cost": card.mana_cost,
            "message": None,
            "error_message": None,
        }
        for card in scryfall_cards
    ]
