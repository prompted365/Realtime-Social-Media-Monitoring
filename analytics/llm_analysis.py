"""LLM powered text summarisation via Requesty."""
from __future__ import annotations

import os

from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider


MODEL_NAME = "openai:gpt-3.5-turbo"


async def generate_summary(text: str) -> str:
    """Return a short summary for ``text`` using the Requesty router."""
    base_url = os.getenv("REQUESTY_BASE_URL")
    api_key = os.getenv("REQUESTY_API_KEY")
    if not base_url or not api_key:
        raise ValueError("Requesty configuration not provided")

    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    agent = Agent(MODEL_NAME, provider=provider)
    result = await agent.run(
        f"Summarise the following text in a short paragraph:\n{text}"
    )
    return str(result.output)
