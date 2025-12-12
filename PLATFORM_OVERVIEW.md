# Platform Evaluation and Business Logic Overview

## Current Architecture
- **Entry point**: `main.py` exposes a CLI that orchestrates scraping, analytics, and persistence. It constructs a `ScraperOrchestrator`, loads agents dynamically, runs scraping concurrently, pipes results through analytics, and stores both raw and analyzed records. It prints per-post results alongside aggregate metrics for quick inspection.
- **Orchestration**: `orchestrator/core.py` discovers agent modules under `agents/`, executes them concurrently via `asyncio.to_thread`, and consolidates their outputs. It accepts a pluggable analytics callable and optional async summarizer hook, enabling reuse of a common scrape → analyze → (summarize) pipeline.
- **Scraping agents**: Each module in `agents/` exposes `scrape(query, limit, **config)` returning `(source, text)` tuples. Implementations rely on Playwright and site-specific flows (e.g., Twitter login flow with credentials, Quora answer page parsing), with hard limits to prevent over-scraping.
- **Analytics**: `analytics/sentiment.py` applies a HuggingFace sentiment pipeline when available, falling back to a rule-based classifier to keep tests lightweight. It attaches sentiment labels per row and aggregates sentiment counts into dataframe attributes for downstream use.
- **Persistence**: `database/storage.py` writes raw and analyzed records into SQLite tables (configurable via table names and `SOCIAL_DB_PATH`). Tables are created lazily; inserts append new rows without mutating existing data.

## Business Logic Highlights
- **Data contract**: Agents must emit `(source, text)` pairs; analytics expects these columns to produce sentiment labels and metrics. The database schema mirrors this contract and persists provenance (`source`) for auditability.
- **Credential handling**: Sensitive values (e.g., Twitter username/password) are pulled from environment variables or injected via config, aligning with the root guideline to avoid hard-coding secrets.
- **Concurrency and limits**: Scraping runs concurrently across agents, and each agent enforces a per-run post cap via `limit` to bound scraping costs and respect site load.
- **Extensibility**: New channels can be added by dropping modules into `agents/` without touching the orchestrator. Analytics functions are injectable, allowing future NLP features (entity extraction, topic modeling) without changing scraping code.

## Observed Gaps and Risks
- **Reliability**: Playwright-dependent agents can fail without browser binaries or valid credentials; retries and richer error reporting would improve robustness.
- **Testing**: There is no automated test coverage for agent discovery, analytics correctness, or database writes, and `pytest`/`flake8` guidance in the root AGENTS is not currently enforced.
- **Data quality**: Scrapers lack normalization, deduplication, and timezone-aware timestamps; adding metadata would strengthen analytics and compliance reporting.
- **Operational safeguards**: Rate-limiting, respectful delays, and terms-of-service considerations are implicit but not codified; explicit policies would clarify acceptable use.

## Recommendations for Merge Readiness
- Add lightweight mocks or fixtures to validate agent discovery and the scrape → analyze → store pipeline end-to-end.
- Introduce structured logging around scraping and persistence to expose failures early and aid observability.
- Provide configuration templates for credentials, database paths, and scraping limits to streamline deployment across environments.
- Expand analytics to include summarization, entity recognition, and trend metrics, retaining the pluggable interface already present in the orchestrator.
