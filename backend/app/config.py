"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import List, Optional
import json


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str
    database_url_sync: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ai_model: str = "gpt-4-turbo-preview"

    # App
    secret_key: str
    cors_origins: List[str] = ["http://localhost:3000"]
    debug: bool = False

    # Rate Limiting
    rate_limit_per_minute: int = 10
    rate_limit_per_day: int = 100

    # Cache TTL
    topic_cache_ttl: int = 3600
    connection_cache_ttl: int = 86400

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.cors_origins, str):
            try:
                self.cors_origins = json.loads(self.cors_origins)
            except json.JSONDecodeError:
                self.cors_origins = [self.cors_origins]


settings = Settings()
