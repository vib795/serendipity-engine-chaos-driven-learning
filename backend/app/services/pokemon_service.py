"""Pokémon API service."""

import httpx
import random
from app.services.topic_fetcher import Topic, TopicSource


class PokemonService:
    """Service for fetching Pokémon data."""

    BASE_URL = "https://pokeapi.co/api/v2"
    MAX_POKEMON_ID = 1010  # Current max Pokemon ID

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    async def fetch_random(self) -> Topic:
        """Fetch a random Pokémon with its lore."""
        pokemon_id = random.randint(1, self.MAX_POKEMON_ID)

        # Fetch basic info
        pokemon_response = await self.client.get(f"{self.BASE_URL}/pokemon/{pokemon_id}")
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()

        # Fetch species info for flavor text
        species_response = await self.client.get(f"{self.BASE_URL}/pokemon-species/{pokemon_id}")
        species_response.raise_for_status()
        species_data = species_response.json()

        # Get English flavor text
        flavor_texts = [
            entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            for entry in species_data.get("flavor_text_entries", [])
            if entry.get("language", {}).get("name") == "en"
        ]

        summary = flavor_texts[0] if flavor_texts else "A mysterious Pokémon."
        full_content = " ".join(flavor_texts[:3]) if len(flavor_texts) > 1 else summary

        # Get types as tags
        types = [t["type"]["name"] for t in pokemon_data.get("types", [])]

        return Topic(
            source=TopicSource.POKEMON,
            source_id=str(pokemon_id),
            title=f"{pokemon_data['name'].title()} (Pokémon)",
            summary=summary,
            full_content=full_content,
            category="Pokémon",
            tags=types + ["pokemon", "creature", "game"],
            image_url=pokemon_data.get("sprites", {})
            .get("other", {})
            .get("official-artwork", {})
            .get("front_default"),
            source_url=f"https://pokemon.com/us/pokedex/{pokemon_data['name']}",
        )
