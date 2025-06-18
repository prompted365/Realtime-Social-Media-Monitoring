from typing import List, Tuple
from playwright.sync_api import sync_playwright


def scrape(query: str, limit: int, **_config) -> List[Tuple[str, str]]:
    """Scrape Reddit posts for ``query``."""
    search = "+".join(query.split())
    url = (
        "https://www.reddit.com/search/?q={}&type=link&sort=new".format(search)
    )
    posts: List[Tuple[str, str]] = []
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(url)
        page.wait_for_selector("faceplate-tracker[aria-posinset='1']")
        for idx in range(1, limit):
            try:
                page.wait_for_selector(
                    f"faceplate-tracker[aria-posinset='{idx}']", timeout=3000
                )
                post_el = page.query_selector(
                    f"faceplate-tracker[aria-posinset='{idx}']"
                )
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                text_el = post_el.query_selector("span[class='invisible']")
                if text_el is not None:
                    posts.append(("Reddit", text_el.text_content()))
            except Exception:
                continue
    return posts
