"""Topic fetcher service - aggregates random topics from multiple sources."""

import asyncio
import random
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum


class TopicSource(str, Enum):
    """Available topic sources."""

    WIKIPEDIA = "wikipedia"
    POKEMON = "pokemon"
    TRIVIA = "trivia"
    FACT = "fact"
    NUMBER = "number"
    QUOTE = "quote"


@dataclass
class Topic:
    """A topic from an external source."""

    source: TopicSource
    source_id: Optional[str]
    title: str
    summary: str
    full_content: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    source_url: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "source": self.source.value if isinstance(self.source, TopicSource) else self.source,
            "source_id": self.source_id,
            "title": self.title,
            "summary": self.summary,
            "full_content": self.full_content,
            "category": self.category,
            "tags": self.tags,
            "image_url": self.image_url,
            "source_url": self.source_url,
        }


class TopicFetcher:
    """
    Aggregates random topics from multiple sources.
    The heart of the serendipity - pulling from diverse domains.
    """

    def __init__(
        self,
        wikipedia_service,
        pokemon_service,
        trivia_service,
        facts_service,
        numbers_service,
        quotes_service,
    ):
        self.services = {
            TopicSource.WIKIPEDIA: wikipedia_service,
            TopicSource.POKEMON: pokemon_service,
            TopicSource.TRIVIA: trivia_service,
            TopicSource.FACT: facts_service,
            TopicSource.NUMBER: numbers_service,
            TopicSource.QUOTE: quotes_service,
        }

        # Weight different sources for variety
        # Higher weight = more likely to be selected
        self.source_weights = {
            TopicSource.WIKIPEDIA: 3.0,  # Rich content, high variety
            TopicSource.POKEMON: 1.5,  # Fun, recognizable
            TopicSource.TRIVIA: 2.0,  # Educational
            TopicSource.FACT: 1.5,  # Quick interesting bits
            TopicSource.NUMBER: 1.0,  # Mathematical angles
            TopicSource.QUOTE: 1.5,  # Philosophical depth
        }

    async def fetch_random_topic(
        self, source: Optional[TopicSource] = None, exclude_sources: List[TopicSource] = None
    ) -> Topic:
        """
        Fetch a single random topic, optionally from a specific source.
        """
        if exclude_sources is None:
            exclude_sources = []

        if source is None:
            # Weighted random selection
            available_sources = [s for s in TopicSource if s not in exclude_sources]
            weights = [self.source_weights[s] for s in available_sources]
            source = random.choices(available_sources, weights=weights, k=1)[0]

        service = self.services[source]
        return await service.fetch_random()

    async def fetch_topic_pair(self, ensure_different_sources: bool = True) -> tuple[Topic, Topic]:
        """
        Fetch two random topics for connection generation.

        By default, ensures topics come from different sources
        to maximize serendipity potential.
        """
        topic_a = await self.fetch_random_topic()

        exclude = [topic_a.source] if ensure_different_sources else []
        topic_b = await self.fetch_random_topic(exclude_sources=exclude)

        return topic_a, topic_b

    async def fetch_multiple_topics(self, count: int = 5, diverse: bool = True) -> List[Topic]:
        """
        Fetch multiple random topics.
        If diverse=True, tries to get topics from different sources.
        """
        if diverse and count <= len(TopicSource):
            # Get one from each source up to count
            sources = random.sample(list(TopicSource), count)
            tasks = [self.fetch_random_topic(source=source) for source in sources]
        else:
            tasks = [self.fetch_random_topic() for _ in range(count)]

        return await asyncio.gather(*tasks)
