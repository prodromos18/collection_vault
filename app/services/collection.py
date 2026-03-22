import logging
from app.models.card import SkryfallCard
from app.services.scryfall import fetch_card_data_by_name
from app.db.repositories.collection_repo import (
    add_to_collection_with_scryfall,
    lookup_card_in_db,
    lookup_card_in_db_by_param,
    fuzzy_search_collection,
    delete_from_collection,
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

def search_cards_by_name(name: str):
    session = SessionLocal()
    matches = fuzzy_search_collection(session, name)
    return [
        {
            "scryfall_id": scryfall_card.scryfall_id,
            "name": scryfall_card.name,
            "type_line": scryfall_card.type_line,
            "mana_cost": scryfall_card.mana_cost,
            "quantity": collection_card.quantity,
        }
        for scryfall_card, collection_card in matches
    ]

def delete_card(scryfall_id: str, quantity: float = None):
    session = SessionLocal()
    scryfall_card = session.query(SkryfallCard).filter_by(scryfall_id=scryfall_id).first()
    if not scryfall_card:
        return None
    card_name = scryfall_card.name
    result = delete_from_collection(session, scryfall_id, quantity)
    if result is None:
        return None
    deleted_quantity = result.get("deleted_quantity") if not result["partial"] else quantity
    return {
        "message": "deleted",
        "name": card_name,
        "quantity": deleted_quantity,
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
