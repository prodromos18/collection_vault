from app.models.card import CollectionCard, SkryfallCard
from sqlalchemy.orm import Session

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
        # return scryfall_id to query the CollectionCard table
        scryfall_card = (session.query(SkryfallCard).filter_by(name=name).first())
        result=session.query(CollectionCard).filter_by(scryfall_id=scryfall_card.scryfall_id).first()
    except Exception as e:
        raise ValueError(f"Error while looking up card in db with name {name}, error: {e}")

    if result:    
        return scryfall_card
