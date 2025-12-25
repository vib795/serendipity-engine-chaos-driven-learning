"""Connection API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import uuid

from app.database import get_db
from app.models.connection import Connection as ConnectionModel
from app.models.topic import Topic as TopicModel
from app.schemas.connection import GenerateConnectionResponse, Connection, ConnectionResponse
from app.schemas.topic import Topic

router = APIRouter()


@router.post("/generate", response_model=GenerateConnectionResponse)
async def generate_connection(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a new random connection between two topics.

    This is the main endpoint that:
    1. Fetches two random topics from different sources
    2. Generates an AI connection between them
    3. Saves everything to the database
    4. Returns the complete result
    """
    # Get services from app state
    topic_fetcher = request.app.state.topic_fetcher
    connection_generator = request.app.state.connection_generator

    # Fetch two random topics
    topic_a_data, topic_b_data = await topic_fetcher.fetch_topic_pair()

    # Save topics to database
    topic_a_dict = topic_a_data.to_dict()
    topic_b_dict = topic_b_data.to_dict()

    # Check if topics already exist
    topic_a_existing = await db.execute(
        select(TopicModel).where(
            TopicModel.source == topic_a_dict["source"],
            TopicModel.title == topic_a_dict["title"],
        )
    )
    topic_a_model = topic_a_existing.scalar_one_or_none()

    if not topic_a_model:
        topic_a_model = TopicModel(**topic_a_dict)
        db.add(topic_a_model)
        await db.flush()

    topic_b_existing = await db.execute(
        select(TopicModel).where(
            TopicModel.source == topic_b_dict["source"],
            TopicModel.title == topic_b_dict["title"],
        )
    )
    topic_b_model = topic_b_existing.scalar_one_or_none()

    if not topic_b_model:
        topic_b_model = TopicModel(**topic_b_dict)
        db.add(topic_b_model)
        await db.flush()

    # Generate AI connection
    generated = await connection_generator.generate_connection(topic_a_data, topic_b_data)

    # Save connection to database
    connection_model = ConnectionModel(
        topic_a_id=topic_a_model.id,
        topic_b_id=topic_b_model.id,
        connection_title=generated.title,
        connection_summary=generated.summary,
        connection_detailed=generated.detailed_explanation,
        connection_type=generated.connection_type,
        bridge_concepts=generated.bridge_concepts,
        creativity_score=generated.creativity_score,
        plausibility_score=generated.plausibility_score,
        model_used=generated.model_used,
        generation_time_ms=generated.generation_time_ms,
        prompt_tokens=generated.prompt_tokens,
        completion_tokens=generated.completion_tokens,
    )

    db.add(connection_model)
    await db.commit()
    await db.refresh(connection_model)
    await db.refresh(topic_a_model)
    await db.refresh(topic_b_model)

    # Return response
    return GenerateConnectionResponse(
        topic_a=Topic.model_validate(topic_a_model),
        topic_b=Topic.model_validate(topic_b_model),
        connection=Connection.model_validate(connection_model),
    )


@router.get("/{connection_id}", response_model=ConnectionResponse)
async def get_connection(
    connection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific connection by ID."""
    result = await db.execute(select(ConnectionModel).where(ConnectionModel.id == connection_id))
    connection = result.scalar_one_or_none()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")

    # Increment view count
    connection.view_count += 1
    await db.commit()

    # Get topics
    topic_a_result = await db.execute(select(TopicModel).where(TopicModel.id == connection.topic_a_id))
    topic_a = topic_a_result.scalar_one()

    topic_b_result = await db.execute(select(TopicModel).where(TopicModel.id == connection.topic_b_id))
    topic_b = topic_b_result.scalar_one()

    return ConnectionResponse(
        connection=Connection.model_validate(connection),
        topic_a=Topic.model_validate(topic_a),
        topic_b=Topic.model_validate(topic_b),
    )


@router.get("/", response_model=List[ConnectionResponse])
async def list_connections(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """List connections (paginated)."""
    result = await db.execute(
        select(ConnectionModel)
        .order_by(desc(ConnectionModel.created_at))
        .offset(skip)
        .limit(limit)
    )
    connections = result.scalars().all()

    responses = []
    for connection in connections:
        topic_a_result = await db.execute(
            select(TopicModel).where(TopicModel.id == connection.topic_a_id)
        )
        topic_a = topic_a_result.scalar_one()

        topic_b_result = await db.execute(
            select(TopicModel).where(TopicModel.id == connection.topic_b_id)
        )
        topic_b = topic_b_result.scalar_one()

        responses.append(
            ConnectionResponse(
                connection=Connection.model_validate(connection),
                topic_a=Topic.model_validate(topic_a),
                topic_b=Topic.model_validate(topic_b),
            )
        )

    return responses


@router.get("/popular", response_model=List[ConnectionResponse])
async def popular_connections(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Get most favorited connections."""
    result = await db.execute(
        select(ConnectionModel)
        .order_by(desc(ConnectionModel.favorite_count), desc(ConnectionModel.created_at))
        .limit(limit)
    )
    connections = result.scalars().all()

    responses = []
    for connection in connections:
        topic_a_result = await db.execute(
            select(TopicModel).where(TopicModel.id == connection.topic_a_id)
        )
        topic_a = topic_a_result.scalar_one()

        topic_b_result = await db.execute(
            select(TopicModel).where(TopicModel.id == connection.topic_b_id)
        )
        topic_b = topic_b_result.scalar_one()

        responses.append(
            ConnectionResponse(
                connection=Connection.model_validate(connection),
                topic_a=Topic.model_validate(topic_a),
                topic_b=Topic.model_validate(topic_b),
            )
        )

    return responses
