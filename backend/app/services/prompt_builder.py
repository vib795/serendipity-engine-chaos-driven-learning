"""Prompt builder for AI connection generation."""

from app.services.topic_fetcher import Topic


class PromptBuilder:
    """
    Constructs prompts for the AI connection generator.
    The quality of connections depends heavily on prompt engineering.
    """

    STYLE_INSTRUCTIONS = {
        "intellectual": """
            Focus on finding deep, substantive connections that reveal genuine
            patterns in knowledge. Look for shared principles, parallel structures,
            historical influences, or conceptual isomorphisms. The connection should
            make the reader feel they've gained real insight.
        """,
        "playful": """
            Find connections that are surprising and delightful. It's okay to be
            a bit whimsical, but the connection should still have a kernel of truth.
            Aim for "Huh, that's actually kind of true!" reactions.
        """,
        "philosophical": """
            Explore deeper meanings and existential parallels. Look for connections
            that touch on fundamental aspects of human experience, consciousness,
            or the nature of reality. Be profound but accessible.
        """,
    }

    def build_system_prompt(self, style: str = "intellectual") -> str:
        """Build the system prompt for the AI."""
        style_instruction = self.STYLE_INSTRUCTIONS.get(style, self.STYLE_INSTRUCTIONS["intellectual"])

        return f"""You are the Serendipity Engine, an AI designed to find unexpected
but genuine intellectual connections between seemingly unrelated topics.

Your purpose is to reveal the hidden threads that connect all knowledge. You find
the surprising parallels, the shared deep structures, and the conceptual bridges
that make people see the world differently.

{style_instruction}

IMPORTANT GUIDELINES:
1. The connection must be GENUINE - not forced, not a stretch, not a joke
2. Find multiple types of connections if possible (historical, conceptual, structural)
3. Explain WHY the connection is meaningful, not just THAT it exists
4. Use specific details from both topics to ground the connection
5. The reader should learn something new about BOTH topics through the connection

You must respond in valid JSON format with this structure:
{{
    "title": "A catchy, intriguing headline (max 100 chars)",
    "summary": "A 1-2 sentence hook that captures the essence",
    "detailed_explanation": "A 2-4 paragraph exploration of the connection",
    "connection_type": "one of: thematic, historical, scientific, metaphorical, structural, cultural",
    "bridge_concepts": ["list", "of", "3-5", "key", "linking concepts"],
    "creativity_score": 0.0-1.0 (how creative/unexpected is this connection),
    "plausibility_score": 0.0-1.0 (how believable/grounded is this connection)
}}
"""

    def build_user_prompt(self, topic_a: Topic, topic_b: Topic) -> str:
        """Build the user prompt with the two topics."""
        return f"""Find the serendipitous connection between these two topics:

=== TOPIC A: {topic_a.title} ===
Source: {topic_a.source.value if hasattr(topic_a.source, 'value') else topic_a.source}
Summary: {topic_a.summary}
{f"Additional context: {topic_a.full_content}" if topic_a.full_content and topic_a.full_content != topic_a.summary else ""}
{f"Tags: {', '.join(topic_a.tags)}" if topic_a.tags else ""}

=== TOPIC B: {topic_b.title} ===
Source: {topic_b.source.value if hasattr(topic_b.source, 'value') else topic_b.source}
Summary: {topic_b.summary}
{f"Additional context: {topic_b.full_content}" if topic_b.full_content and topic_b.full_content != topic_b.summary else ""}
{f"Tags: {', '.join(topic_b.tags)}" if topic_b.tags else ""}

Find the unexpected intellectual bridge between these topics. What do they
reveal about each other? What shared truth or pattern connects them?
"""
