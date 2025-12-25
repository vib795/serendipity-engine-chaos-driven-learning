"""Quotes API service."""

import httpx
from app.services.topic_fetcher import Topic, TopicSource


class QuotesService:
    """Service for fetching quotes."""

    BASE_URL = "https://api.quotable.io"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    async def fetch_random(self) -> Topic:
        """Fetch a random quote."""
        response = await self.client.get(f"{self.BASE_URL}/random")
        response.raise_for_status()
        data = response.json()

        author = data.get("author", "Unknown")
        content = data.get("content", "")

        return Topic(
            source=TopicSource.QUOTE,
            source_id=data.get("_id"),
            title=f"Quote by {author}",
            summary=f'"{content}" — {author}',
            full_content=content,
            category="Philosophy",
            tags=data.get("tags", []) + ["quote", "wisdom"],
        )
