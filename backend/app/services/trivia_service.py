"""Trivia API service."""

import httpx
import html
from app.services.topic_fetcher import Topic, TopicSource


class TriviaService:
    """Service for fetching trivia questions."""

    BASE_URL = "https://opentdb.com/api.php"

    CATEGORIES = {
        9: "General Knowledge",
        17: "Science & Nature",
        18: "Computers",
        19: "Mathematics",
        20: "Mythology",
        21: "Sports",
        22: "Geography",
        23: "History",
        24: "Politics",
        25: "Art",
        26: "Celebrities",
        27: "Animals",
    }

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    async def fetch_random(self) -> Topic:
        """Fetch a random trivia question as a topic."""
        response = await self.client.get(self.BASE_URL, params={"amount": 1, "type": "multiple"})
        response.raise_for_status()
        data = response.json()

        if data.get("response_code") != 0 or not data.get("results"):
            raise Exception("Failed to fetch trivia")

        trivia = data["results"][0]

        # Decode HTML entities
        question = html.unescape(trivia["question"])
        answer = html.unescape(trivia["correct_answer"])
        category = html.unescape(trivia["category"])

        return Topic(
            source=TopicSource.TRIVIA,
            source_id=None,  # Trivia API doesn't provide IDs
            title=f"Trivia: {question}",
            summary=f"The answer is: {answer}",
            full_content=f"Question: {question}\n\nAnswer: {answer}\n\nCategory: {category}",
            category=category,
            tags=[category.lower(), trivia["difficulty"], "trivia"],
        )
