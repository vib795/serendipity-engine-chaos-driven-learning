"""Main API router."""

from fastapi import APIRouter
from app.api import connections, topics

api_router = APIRouter()

api_router.include_router(connections.router, prefix="/connections", tags=["connections"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
