import os
from typing import List, Tuple
from urllib.parse import quote
import time
from playwright.sync_api import sync_playwright


def scrape(query: str, limit: int, **config) -> List[Tuple[str, str]]:
    """Scrape tweets for a query using Playwright.

    Credentials are loaded from environment variables TWITTER_USERNAME and
    TWITTER_PASSWORD unless provided via ``config``.
    """
    username = config.get("username") or os.getenv("TWITTER_USERNAME")
    password = config.get("password") or os.getenv("TWITTER_PASSWORD")
    if not username or not password:
        raise ValueError("Twitter credentials not provided")

    search = quote(query)
    login_url = (
        "https://twitter.com/i/flow/login?input_flow_data=%7B%22"
        "requested_variant%22%3A%22eyJsYW5nIjoiZW4ifQ%3D%3D%22%7D"
    )
    url = f"https://twitter.com/search?q={search}&src=recent_search_click&f=live"

    posts: List[Tuple[str, str]] = []
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(login_url)
        page.wait_for_load_state("networkidle")
        page.fill("input[name='text']", username)
        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle")
        try:
            page.fill("input[name='text']", username)
            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle")
        except Exception:
            pass
        page.fill("input[name='password']", password)
        page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle")

        time.sleep(5)
        page.goto(url)
        time.sleep(2)

        for idx in range(1, min(limit, 25)):
            try:
                page.wait_for_selector(
                    f"div[data-testid='cellInnerDiv']:nth-child({idx})", timeout=3000
                )
                post_text = page.query_selector(
                    f"div[data-testid='cellInnerDiv']:nth-child({idx}) div[data-testid='tweetText']"
                )
                if post_text is not None:
                    posts.append(("Twitter", post_text.text_content()))
                page.keyboard.press("PageDown")
                time.sleep(1)
            except Exception:
                continue
    return posts
