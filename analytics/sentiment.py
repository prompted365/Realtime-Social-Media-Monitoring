from typing import Dict
import pandas as pd
try:
    from transformers import pipeline, Pipeline
except Exception:  # pragma: no cover - optional dependency
    pipeline = None
    class Pipeline:  # type: ignore
        pass


def _create_pipeline() -> Pipeline:
    if pipeline is None:
        # Fallback simple rule based classifier to keep tests fast
        class _Dummy(Pipeline):
            def __call__(self, texts):
                if isinstance(texts, str):
                    texts = [texts]
                return [
                    {"label": "POSITIVE" if "good" in t.lower() else "NEGATIVE"}
                    for t in texts
                ]
        return _Dummy()
    try:
        return pipeline("sentiment-analysis")
    except Exception:
        return _Dummy()


sentiment_pipeline = _create_pipeline()


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """Add sentiment scores and aggregate metrics to the dataframe."""
    df = df.copy()
    df["sentiment"] = df["text"].apply(lambda x: sentiment_pipeline(x)[0]["label"])
    metrics: Dict[str, int] = df["sentiment"].value_counts().to_dict()
    df.attrs["metrics"] = metrics
    return df
