"""Wikipedia API service."""

import httpx
from typing import Optional
from app.services.topic_fetcher import Topic, TopicSource
from app.utils.cache import cache


class WikipediaService:
    """Service for fetching Wikipedia articles."""

    BASE_URL = "https://en.wikipedia.org/api/rest_v1"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    @cache(ttl=3600)  # Cache for 1 hour
    async def fetch_random(self) -> Topic:
        """Fetch a random Wikipedia article summary."""
        response = await self.client.get(
            f"{self.BASE_URL}/page/random/summary",
            headers={"User-Agent": "SerendipityEngine/1.0 (educational project)"},
        )
        response.raise_for_status()
        data = response.json()

        return Topic(
            source=TopicSource.WIKIPEDIA,
            source_id=str(data.get("pageid")),
            title=data.get("title", "Unknown"),
            summary=data.get("extract", ""),
            full_content=data.get("extract"),
            image_url=data.get("thumbnail", {}).get("source") if data.get("thumbnail") else None,
            source_url=data.get("content_urls", {}).get("desktop", {}).get("page"),
            tags=self._extract_tags(data),
        )

    def _extract_tags(self, data: dict) -> list:
        """Extract relevant tags from Wikipedia data."""
        tags = ["wikipedia"]
        if data.get("type"):
            tags.append(data["type"])
        return tags
