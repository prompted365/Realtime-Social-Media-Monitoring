import pytest

from agents.twitter_agent import scrape as twitter
from agents.facebook_agent import scrape as facebook


def test_twitter_missing_env(monkeypatch):
    monkeypatch.delenv("TWITTER_USERNAME", raising=False)
    monkeypatch.delenv("TWITTER_PASSWORD", raising=False)
    with pytest.raises(ValueError):
        twitter("query", 1)


def test_facebook_missing_env(monkeypatch):
    monkeypatch.delenv("TWITTER_USERNAME", raising=False)
    monkeypatch.delenv("TWITTER_PASSWORD", raising=False)
    with pytest.raises(ValueError):
        facebook("query", 1)
