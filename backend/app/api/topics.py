"""Topic API endpoints."""

from fastapi import APIRouter, Request
from typing import Optional, List

from app.schemas.topic import Topic
from app.services.topic_fetcher import TopicSource

router = APIRouter()


@router.get("/random", response_model=List[Topic])
async def get_random_topics(
    request: Request,
    count: int = 2,
    diverse: bool = True,
):
    """Get multiple random topics."""
    topic_fetcher = request.app.state.topic_fetcher
    topics = await topic_fetcher.fetch_multiple_topics(count=count, diverse=diverse)
    return [Topic(**t.to_dict()) for t in topics]


@router.get("/random/{source}", response_model=Topic)
async def get_random_topic_from_source(
    request: Request,
    source: TopicSource,
):
    """Get a random topic from a specific source."""
    topic_fetcher = request.app.state.topic_fetcher
    topic = await topic_fetcher.fetch_random_topic(source=source)
    return Topic(**topic.to_dict())
