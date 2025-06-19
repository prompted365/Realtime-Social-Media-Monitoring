import os
import sqlite3
from typing import Iterable, Tuple

DB_PATH = os.getenv("SOCIAL_DB_PATH", "social_media.db")


def _connect(db_path: str = DB_PATH):
    return sqlite3.connect(db_path)


def store_raw(table: str, rows: Iterable[Tuple[str, str]]) -> None:
    """Persist raw scraped posts.

    The table is created on first use and subsequent calls simply
    append new records without altering existing rows.
    """
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ("
            "id INTEGER PRIMARY KEY, source TEXT, text TEXT)"
        )
        cur.executemany(
            f"INSERT INTO {table} (source, text) VALUES (?, ?)", rows
        )
        conn.commit()


def store_analysis(table: str, df) -> None:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ("
            "id INTEGER PRIMARY KEY, "
            "source TEXT, text TEXT, sentiment TEXT)"
        )
        for _, row in df.iterrows():
            cur.execute(
                f"INSERT INTO {table} (source, text, sentiment) VALUES (?,?,?)",
                (row["source"], row["text"], row["sentiment"]),
            )
        conn.commit()
