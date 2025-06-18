# Agentic Development Guidelines

This file outlines the plans and conventions for extending the **Realtime Social Media Monitoring** project with a more agent‑driven architecture.

## Goals
- Introduce an orchestrator that can manage and route scraping agents and analytic agents.
- Expand scraping coverage beyond Twitter, Facebook, Reddit and Quora.
- Provide advanced NLP analytics for strategic insight.
- Maintain modular, testable components and consistent data storage.

## Modular Agents
- Place new scraping agents under `agents/` with the pattern `<channel>_agent.py`.
- Each agent exposes `scrape(query: str, limit: int, **config) -> List[Tuple[str, str]]` and handles its own authentication via environment variables or configuration files.
- Avoid hard‑coded credentials.

## Orchestration Layer
- Implement an `orchestrator/` package responsible for invoking scraping agents and analytics modules.
- Support asynchronous execution using `asyncio` or a job queue.
- Allow dynamic registration of agents so new channels can be added without modifying the orchestrator core.

## NLP Analytics
- Move the current sentiment logic into an `analytics/` package.
- Extend analytics with entity recognition, topic modeling, trend detection and summarisation using HuggingFace or similar libraries.
- Provide a unified interface: `analyze(df: pandas.DataFrame) -> pandas.DataFrame` returning results per post and aggregate metrics.

## Database & Persistence
- Centralise database logic under `database/` with models for raw scraped content and analytics results.
- Maintain a single SQLite database by default; support swapping to other backends if required.
- Keep schema consistent across channels; each record stores `source`, `text`, `timestamp`, and any metadata.

## Testing & Quality
- Use `flake8` (or `ruff`) for linting and `pytest` for unit tests.
- Document how to run checks: `flake8` then `pytest`. All tests should pass before committing new features.

## Future API
- Provide a CLI (`main.py`) that loads configuration, starts the orchestrator and runs the desired agents.
- Optionally expose a REST API using FastAPI for programmatic access to scraping and analytics.

