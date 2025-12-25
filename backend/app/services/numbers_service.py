"""Numbers API service."""

import httpx
import random
from app.services.topic_fetcher import Topic, TopicSource


class NumbersService:
    """Service for fetching number facts."""

    BASE_URL = "http://numbersapi.com"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    async def fetch_random(self) -> Topic:
        """Fetch a random number fact."""
        fact_types = ["trivia", "math", "date", "year"]
        fact_type = random.choice(fact_types)

        response = await self.client.get(f"{self.BASE_URL}/random/{fact_type}", params={"json": "true"})
        response.raise_for_status()
        data = response.json()

        number = data.get("number", "unknown")
        fact_text = data.get("text", "")

        return Topic(
            source=TopicSource.NUMBER,
            source_id=f"{fact_type}_{number}",
            title=f"The Number {number}",
            summary=fact_text,
            full_content=fact_text,
            category=fact_type.title(),
            tags=["number", "mathematics", fact_type],
        )
