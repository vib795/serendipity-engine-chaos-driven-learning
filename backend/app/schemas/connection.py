"""Connection schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from app.schemas.topic import Topic


class ConnectionBase(BaseModel):
    """Base connection schema."""

    connection_title: str = Field(alias="title")
    connection_summary: str = Field(alias="summary")
    connection_detailed: str = Field(alias="detailed_explanation")
    connection_type: Optional[str] = None
    bridge_concepts: List[str] = Field(default_factory=list)
    creativity_score: Optional[Decimal] = None
    plausibility_score: Optional[Decimal] = None


class ConnectionCreate(ConnectionBase):
    """Connection creation schema."""

    topic_a_id: UUID
    topic_b_id: UUID
    model_used: Optional[str] = None
    generation_time_ms: Optional[int] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None


class Connection(ConnectionBase):
    """Connection response schema."""

    id: UUID
    topic_a_id: UUID
    topic_b_id: UUID
    view_count: int = 0
    favorite_count: int = 0
    share_count: int = 0
    model_used: Optional[str] = None
    generation_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class ConnectionResponse(BaseModel):
    """Connection response with topics."""

    connection: Connection
    topic_a: Topic
    topic_b: Topic


class GenerateConnectionResponse(BaseModel):
    """Response for generated connection."""

    topic_a: Topic
    topic_b: Topic
    connection: Connection
