from app.models.card import CollectionCard, SkryfallCard
from app.db.repositories.common import OP_MAPPING
from sqlalchemy.orm import Session
from sqlalchemy import func

import logging

logger = logging.getLogger(__name__)

def add_to_collection_with_scryfall(session: Session, card_id, scryfall_card_data, quantity):
    try:
        existing_card = session.query(SkryfallCard).filter_by(
            scryfall_id=card_id).first()
        
        if not existing_card:
            db_card = SkryfallCard(
                scryfall_id=scryfall_card_data.scryfall_id,
                name=scryfall_card_data.name,
                mana_cost=scryfall_card_data.mana_cost,
                type_line=scryfall_card_data.type_line,
                oracle_text=scryfall_card_data.oracle_text,
                image_url=scryfall_card_data.image_url
            )
            session.add(db_card)
            # get the ID without committing yet
            session.flush()
        else:
            logger.info(f"Card {scryfall_card_data.name} already exists in db")

        collection_card = CollectionCard(scryfall_id=card_id, quantity=quantity)
        session.add(collection_card)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def add_scryfall_card_to_db(session: Session, scryfall_card: SkryfallCard):
    try:
        session.add(scryfall_card)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def lookup_card_in_db(session: Session, name: str):
    try:
        # return scryfall_id to query the CollectionCard table using fuzzy search
        # through the pg_trgm extension. Returns the match with the highest similarity
        scryfall_card = (
        session.query(SkryfallCard)
        .filter(func.similarity(SkryfallCard.name, name) > 0.3)
        .order_by(func.similarity(SkryfallCard.name, name).desc())
        .first()
    )
        if scryfall_card:
            logger.info(f"A card with a similar name to {name} exists in the magic realm {(scryfall_card.name)}")
        else:
            logger.info(f"A card with a name like {name} does not exist in MTG")
        result=session.query(CollectionCard).filter_by(scryfall_id=scryfall_card.scryfall_id).first()
    except Exception as e:
        raise ValueError(f"Error while looking up card in db with name {name}, error: {e}")

    if result:    
        return scryfall_card

def lookup_card_in_db_by_param(session: Session, **kwargs):
    try:
        # construct the query according to the search criteria provided by the user
        # criteria consist of field name mapped to operator and value:
        # {
        #   "mana_cost": {"op": "gte", "value": 3},
        #   "type_line": {"op": "contains", "value": "Creature"}
        # }
        filters = []
        for field_name, criterion in kwargs.items():
            op_func = OP_MAPPING[criterion["op"]]
            value = criterion["value"]
            column = getattr(SkryfallCard, field_name)
            expression = op_func(column, value)
            filters.append(expression)

        results = (
            session.query(SkryfallCard)
            .join(CollectionCard, CollectionCard.scryfall_id == SkryfallCard.scryfall_id)
            .filter(*filters)
            .all()
        )
        return results
    except Exception as e:
        raise ValueError(f"Error while looking up cards by parameters, error: {e}")