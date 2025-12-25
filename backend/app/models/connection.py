"""Connection model."""

from sqlalchemy import Column, String, Text, Integer, DateTime, Index, ARRAY, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Connection(Base):
    """Generated connection between two topics."""

    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # The two topics being connected
    topic_a_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    topic_b_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    topic_a = relationship("Topic", foreign_keys=[topic_a_id])
    topic_b = relationship("Topic", foreign_keys=[topic_b_id])

    # The AI-generated connection
    connection_title = Column(String(500), nullable=False)
    connection_summary = Column(Text, nullable=False)
    connection_detailed = Column(Text, nullable=False)

    # Connection metadata
    connection_type = Column(String(50), nullable=True)  # 'thematic', 'historical', etc.
    bridge_concepts = Column(ARRAY(Text), nullable=True, default=[])

    # Quality metrics
    creativity_score = Column(Numeric(3, 2), nullable=True)
    plausibility_score = Column(Numeric(3, 2), nullable=True)

    # User engagement
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)

    # AI metadata
    model_used = Column(String(50), nullable=True)
    generation_time_ms = Column(Integer, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_connections_created_at", "created_at"),
        Index("idx_connections_favorite_count", "favorite_count"),
        Index("idx_connections_topics", "topic_a_id", "topic_b_id", unique=True),
    )
