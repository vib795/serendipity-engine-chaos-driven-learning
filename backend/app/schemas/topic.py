"""Topic schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TopicBase(BaseModel):
    """Base topic schema."""

    source: str
    source_id: Optional[str] = None
    title: str
    summary: str
    full_content: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)


class TopicCreate(TopicBase):
    """Topic creation schema."""

    pass


class Topic(TopicBase):
    """Topic response schema."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    """Topic response wrapper."""

    topic: Topic
