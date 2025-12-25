"""User schemas."""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: Optional[str] = None


class User(UserBase):
    """User response schema."""

    id: UUID
    connections_generated: int = 0
    favorites_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response wrapper."""

    user: User
