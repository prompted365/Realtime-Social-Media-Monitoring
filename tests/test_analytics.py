import pandas as pd
from analytics.sentiment import analyze


def test_analyze_adds_sentiment_and_metrics():
    df = pd.DataFrame(
        [("Twitter", "Good"), ("Twitter", "Bad")], columns=["source", "text"]
    )
    result = analyze(df)
    assert "sentiment" in result.columns
    assert isinstance(result.attrs.get("metrics"), dict)
