# Agent-Specific Guidelines

These rules apply to all files under `agents/` and merge the platform's technical and business logic.

## Core Expectations
- Export a `scrape(query: str, limit: int, **config) -> list[tuple[str, str]]` function; return `(source, text)` pairs so analytics and storage layers remain interoperable.
- Use environment variables or injected `config` for credentials and API keys; never hard-code secrets or tokens.
- Respect per-call `limit` values to contain operational cost and site load. Favor bounded selectors/pagination over deep scrolling.
- Keep Playwright/browser automation resilient: wait for network idle states, surface meaningful errors, and prefer lightweight selectors that survive minor DOM shifts.

## Data Quality & Compliance
- Normalize whitespace and strip boilerplate where feasible to reduce noise in downstream analytics.
- Capture optional metadata when available (e.g., timestamps, permalinks) but avoid PII; ensure scraping aligns with each site's terms of service.
- Add basic deduplication if sites frequently repeat content within a session to protect storage and metric accuracy.

## Extensibility
- Encapsulate channel-specific helpers (selectors, login flows) inside each module to minimize shared state between agents.
- When adding new channels, document any prerequisites (cookies, auth steps, rate limits) at the top of the file for quick onboarding.
- Prefer small, pure helpers that are easy to unit test with mocked Playwright/page objects; avoid global mutable state.

## Operational Notes
- Keep dependencies minimal; if a channel requires heavyweight tooling, guard imports and degrade gracefully so other agents can still run.
- Log concise, user-actionable messages from failures (e.g., auth issues, selector timeouts) to help triage without exposing secrets.
