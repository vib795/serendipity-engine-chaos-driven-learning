"""AI-powered connection generator."""

from typing import Optional, List
from dataclasses import dataclass
import json
import time

from openai import AsyncOpenAI

from app.services.topic_fetcher import Topic
from app.services.prompt_builder import PromptBuilder
from app.config import settings


@dataclass
class GeneratedConnection:
    """A generated connection between two topics."""

    title: str  # Catchy headline
    summary: str  # 1-2 sentence hook
    detailed_explanation: str  # Full breakdown
    connection_type: str  # 'thematic', 'historical', etc.
    bridge_concepts: List[str]  # Key linking concepts
    creativity_score: float  # 0-1 self-assessed
    plausibility_score: float  # 0-1 self-assessed
    model_used: str
    generation_time_ms: int
    prompt_tokens: int
    completion_tokens: int


class ConnectionGenerator:
    """
    The AI-powered brain of Serendipity Engine.
    Takes two unrelated topics and finds genuine intellectual bridges.
    """

    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in environment.")

        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.prompt_builder = PromptBuilder()
        self.model = settings.ai_model  # e.g., "gpt-4-turbo-preview"

    async def generate_connection(
        self, topic_a: Topic, topic_b: Topic, style: str = "intellectual"
    ) -> GeneratedConnection:
        """
        Generate a serendipitous connection between two topics.
        """
        start_time = time.time()

        # Build the prompt
        system_prompt = self.prompt_builder.build_system_prompt(style)
        user_prompt = self.prompt_builder.build_user_prompt(topic_a, topic_b)

        # Call the AI
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,  # Higher for creativity
            max_tokens=1500,
            response_format={"type": "json_object"},
        )

        generation_time = int((time.time() - start_time) * 1000)

        # Parse the response
        content = response.choices[0].message.content
        result = json.loads(content)

        return GeneratedConnection(
            title=result["title"],
            summary=result["summary"],
            detailed_explanation=result["detailed_explanation"],
            connection_type=result["connection_type"],
            bridge_concepts=result["bridge_concepts"],
            creativity_score=float(result.get("creativity_score", 0.7)),
            plausibility_score=float(result.get("plausibility_score", 0.7)),
            model_used=self.model,
            generation_time_ms=generation_time,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )
