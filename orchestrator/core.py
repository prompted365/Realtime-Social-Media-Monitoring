import asyncio
import importlib
import pkgutil
from typing import Callable, Coroutine, Dict, List, Tuple

import pandas as pd

import agents


class ScraperOrchestrator:
    """Dynamically loads and runs scraping agents."""

    def __init__(self) -> None:
        self.agents: Dict[str, Callable[[str, int], List[Tuple[str, str]]]] = {}

    def load_agents(self) -> None:
        """Discover agents in the ``agents`` package."""
        for _, mod_name, _ in pkgutil.iter_modules(agents.__path__):
            try:
                module = importlib.import_module(f"agents.{mod_name}")
            except Exception:
                continue
            scrape = getattr(module, "scrape", None)
            if callable(scrape):
                self.agents[mod_name.replace("_agent", "")] = scrape

    async def run(self, query: str, limit: int) -> List[Tuple[str, str]]:
        """Run all registered agents concurrently and gather results."""
        tasks = [asyncio.to_thread(agent, query, limit) for agent in self.agents.values()]
        results: List[List[Tuple[str, str]]] = await asyncio.gather(*tasks)
        combined: List[Tuple[str, str]] = []
        for sub in results:
            combined.extend(sub)
        return combined

    async def scrape_and_analyze(
        self,
        query: str,
        limit: int,
        analyze: Callable[[pd.DataFrame], pd.DataFrame],
        summarize: Callable[[str], Coroutine[None, None, str]] | None = None,
    ) -> pd.DataFrame:
        posts = await self.run(query, limit)
        df = pd.DataFrame(posts, columns=["source", "text"])
        df = analyze(df)
        if summarize is not None:
            text = "\n".join(df["text"].tolist())
            df.attrs["summary"] = await summarize(text)
        return df
