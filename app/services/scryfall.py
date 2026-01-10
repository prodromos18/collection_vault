import re
import requests
import logging
from app.models.card import SkryfallCard
from app.services.configuration import Configuration

logger = logging.getLogger(__name__)
configuration = Configuration()


def fetch_card_data_by_name(name: str) -> SkryfallCard:
    #Scryfall API endpoint for a card by full name
    name = _format_name(name)
    url = f"{configuration.SRYFALL_API_URL}/cards/named?exact={name}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch card data: {response.status_code}")
    elif response.status_code == 200:
        logger.info(f"Card data for {name} have been fetched succesfully")

        data=response.json()

    image_url = ""
    if data.get("image_uris"):
        image_url = data["image_uris"].get("normal", "")
        scryfall_card= SkryfallCard(
            scryfall_id=data.get("id"),
            name=data.get("name"),
            mana_cost=data.get("mana_cost", ""),
            type_line=data.get("type_line", ""),
            oracle_text=data.get("oracle_text", ""),
            image_url=image_url 
        )

    return scryfall_card


def _format_name(name):
    name=name.lower()
    #remove all chars except letters, numbers and spaces
    name = re.sub(r'[^a-z0-9\s]', '', name)
    # Replace one or more spaces with a single hyphen
    name = re.sub(r'\s+', '-', name.strip())
    return name