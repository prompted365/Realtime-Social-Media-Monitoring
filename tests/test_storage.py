import importlib


def test_store_raw_appends(monkeypatch, tmp_path):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("SOCIAL_DB_PATH", str(db_file))
    import database.storage as storage
    importlib.reload(storage)

    storage.store_raw("posts", [("Twitter", "hello")])
    storage.store_raw("posts", [("Twitter", "world")])

    with storage._connect(str(db_file)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT source, text FROM posts")
        rows = cur.fetchall()
    assert rows == [
        ("Twitter", "hello"),
        ("Twitter", "world"),
    ]


def test_store_raw_multiple_batches(monkeypatch, tmp_path):
    """Ensure repeated calls with multiple rows append properly."""
    db_file = tmp_path / "batch.db"
    monkeypatch.setenv("SOCIAL_DB_PATH", str(db_file))
    import database.storage as storage
    importlib.reload(storage)

    batch_one = [("Facebook", "foo"), ("Facebook", "bar")]
    batch_two = [("Reddit", "baz"), ("Reddit", "qux")]

    storage.store_raw("posts", batch_one)
    storage.store_raw("posts", batch_two)

    with storage._connect(str(db_file)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT source, text FROM posts")
        rows = cur.fetchall()
    assert rows == batch_one + batch_two
