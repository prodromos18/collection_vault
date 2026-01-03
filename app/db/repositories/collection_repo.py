from app.models.card import CollectionCard
from app.db.session import SessionLocal

session=SessionLocal()

def add_to_collection(card_id, quantity):
    try:
        collection_card = CollectionCard(scryfall_id=card_id, quantity=quantity)
        session.add(collection_card)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()