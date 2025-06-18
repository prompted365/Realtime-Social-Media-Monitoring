from typing import List, Tuple
from urllib.parse import quote
from playwright.sync_api import sync_playwright


def scrape(query: str, limit: int, **_config) -> List[Tuple[str, str]]:
    """Scrape Quora answers for ``query``."""
    query = quote(query)
    url = f"https://www.quora.com/search?q={query}&type=answer"
    posts: List[Tuple[str, str]] = []
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        selector = "div[class='q-box qu-borderBottom qu-p--medium qu-pb--tiny']"
        text_selector = (
            "div[class='CssComponent__CssInlineComponent-sc-1oskqb9-1 "
            "QTextTruncated___StyledCssInlineComponent-sc-1pev100-1  iRsLoo']"
        )
        for idx in range(1, limit + 1):
            try:
                item = f"{selector}:nth-child({idx+1})"
                page.wait_for_selector(item, timeout=1000)
                post_el = page.query_selector(item)
                text_el = post_el.query_selector(text_selector)
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                if text_el is not None:
                    posts.append(("Quora", text_el.text_content()))
            except Exception:
                continue
    return posts
