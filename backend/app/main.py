"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx

from app.config import settings
from app.api.router import api_router
from app.services.topic_fetcher import TopicFetcher
from app.services.wikipedia_service import WikipediaService
from app.services.pokemon_service import PokemonService
from app.services.trivia_service import TriviaService
from app.services.facts_service import FactsService
from app.services.numbers_service import NumbersService
from app.services.quotes_service import QuotesService
from app.services.connection_generator import ConnectionGenerator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("✨ Serendipity Engine starting up...")

    # Initialize HTTP client
    # Disable SSL verification in development to handle expired certificates
    verify_ssl = not settings.debug
    app.state.http_client = httpx.AsyncClient(
        timeout=30.0,
        verify=verify_ssl,
        follow_redirects=True
    )

    # Initialize services
    http = app.state.http_client
    app.state.topic_fetcher = TopicFetcher(
        wikipedia_service=WikipediaService(http),
        pokemon_service=PokemonService(http),
        trivia_service=TriviaService(http),
        facts_service=FactsService(http),
        numbers_service=NumbersService(http),
        quotes_service=QuotesService(http),
    )
    app.state.connection_generator = ConnectionGenerator()

    print("✨ All services initialized successfully!")

    yield

    # Shutdown
    await app.state.http_client.aclose()
    print("✨ Serendipity Engine shutting down...")


app = FastAPI(
    title="Serendipity Engine API",
    description="Automate serendipity - discover unexpected connections between unrelated topics",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "✨ Serendipity Engine",
        "tagline": "Innovation begins where ideas collide",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "serendipity-engine"}
