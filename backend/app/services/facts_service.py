"""Facts API service."""

import httpx
from app.services.topic_fetcher import Topic, TopicSource


class FactsService:
    """Service for fetching interesting facts."""

    BASE_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    async def fetch_random(self) -> Topic:
        """Fetch a random interesting fact."""
        response = await self.client.get(self.BASE_URL, params={"language": "en"})
        response.raise_for_status()
        data = response.json()

        fact_text = data.get("text", "")

        return Topic(
            source=TopicSource.FACT,
            source_id=data.get("id"),
            title="Interesting Fact",
            summary=fact_text,
            full_content=fact_text,
            source_url=data.get("source_url"),
            tags=["fact", "interesting"],
        )
