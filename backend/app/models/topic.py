"""Topic model."""

from sqlalchemy import Column, String, Text, DateTime, Index, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Topic(Base):
    """Topic from external API sources."""

    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Source information
    source = Column(String(50), nullable=False)  # 'wikipedia', 'pokemon', 'trivia', etc.
    source_id = Column(String(255), nullable=True)

    # Content
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    full_content = Column(Text, nullable=True)

    # Metadata
    category = Column(String(100), nullable=True)
    tags = Column(ARRAY(Text), nullable=True, default=[])
    image_url = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)

    # For enrichment
    keywords = Column(ARRAY(Text), nullable=True, default=[])

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_topics_source", "source"),
        Index("idx_topics_created_at", "created_at"),
        Index("idx_topics_source_id", "source", "source_id", unique=True),
    )
