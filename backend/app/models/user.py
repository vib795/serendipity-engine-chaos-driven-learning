"""User model."""

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class User(Base):
    """User model for favorites and stats."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(255), unique=True, nullable=True)
    username = Column(String(100), unique=True, nullable=True)

    # Optional auth (can be anonymous)
    password_hash = Column(String(255), nullable=True)

    # Stats
    connections_generated = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
