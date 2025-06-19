from types import SimpleNamespace

import pytest

from analytics import llm_analysis
import pydantic_ai.providers.openai as openai_provider
from orchestrator.core import ScraperOrchestrator


class DummyClient:
    def __init__(self, *args, **kwargs):
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self.create)
        )

    async def create(self, *args, **kwargs):
        msg = SimpleNamespace(content="summary", tool_calls=None, reasoning_content=None)
        choice = SimpleNamespace(message=msg, logprobs=None)
        return SimpleNamespace(created=0, choices=[choice], usage=None, model="gpt", id="1")


@pytest.mark.asyncio
async def test_generate_summary(monkeypatch):
    monkeypatch.setenv("REQUESTY_BASE_URL", "http://test")
    monkeypatch.setenv("REQUESTY_API_KEY", "secret")
    monkeypatch.setattr(openai_provider, "AsyncOpenAI", DummyClient)

    result = await llm_analysis.generate_summary("hello world")
    assert result == "summary"


@pytest.mark.asyncio
async def test_orchestrator_uses_summary(monkeypatch):
    orch = ScraperOrchestrator()
    orch.agents = {"dummy": lambda q, limit: [("x", "text1"), ("x", "text2")]}  # type: ignore

    async def dummy_summary(text: str) -> str:
        return "sum"

    df = await orch.scrape_and_analyze(
        "query",
        1,
        lambda df: df,
        summarize=dummy_summary,
    )
    assert df.attrs["summary"] == "sum"
