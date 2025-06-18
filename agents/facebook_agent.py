import os
from typing import List, Tuple
from urllib.parse import quote
from playwright.sync_api import sync_playwright


def scrape(query: str, limit: int, **config) -> List[Tuple[str, str]]:
    """Scrape Facebook posts for ``query``.

    Requires FACEBOOK_EMAIL and FACEBOOK_PASSWORD environment variables or values
    passed via ``config``.
    """
    email = config.get("email") or os.getenv("FACEBOOK_EMAIL")
    password = config.get("password") or os.getenv("FACEBOOK_PASSWORD")
    if not email or not password:
        raise ValueError("Facebook credentials not provided")

    start_url = "https://www.facebook.com/"
    query = quote(query)
    search_url = (
        "https://www.facebook.com/search/posts?q={}".format(query)
    )

    posts: List[Tuple[str, str]] = []
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(start_url)
        page.wait_for_selector("input[name='email']")
        page.fill("input[name='email']", email)
        page.fill("input[name='pass']", password)
        page.click("button[name='login']")
        page.wait_for_load_state("networkidle")
        page.goto(search_url)
        for idx in range(1, limit):
            try:
                page.wait_for_selector(f"div[aria-posinset='{idx}']", timeout=3000)
                post_el = page.query_selector(f"div[aria-posinset='{idx}']")
                if post_el is None:
                    continue
                try:
                    post_el.click("div[role='button']")
                    page.wait_for_load_state("networkidle")
                except Exception:
                    pass
                posts.append(("Facebook", post_el.text_content()))
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            except Exception:
                continue
    return posts
