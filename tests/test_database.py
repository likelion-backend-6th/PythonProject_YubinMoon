from pprint import pprint
import psycopg2
import pytest
from unittest.mock import patch
import setting

setting.DB_NAME = "test_library"
import database


@database.connect
def clear_db(cur):
    cur.execute("DROP TABLE IF EXISTS books;")
    cur.execute("DROP TABLE IF EXISTS loans;")


clear_db()


def test_create_db():
    database.create_tables()
    assert "test_library" in database.get_db_name()


def test_add_book():
    for i in range(10):
        res = database.create_book(
            f"B00{i}", f"test_book{i}", f"test_author{i}", f"test_publisher{i}"
        )
        assert res == i + 1


def test_read_books():
    res = database.read_books()
    for idx, data in enumerate(res):
        assert data == (
            idx + 1,
            f"B00{idx}",
            f"test_book{idx}",
            f"test_author{idx}",
            f"test_publisher{idx}",
            True,
        )

    res = database.read_books(limit=3, offset=2, order_by="title")
    for idx, data in enumerate(res):
        num = idx + 2
        assert data == (
            num + 1,
            f"B00{num}",
            f"test_book{num}",
            f"test_author{num}",
            f"test_publisher{num}",
            True,
        )


def test_update_book():
    res = database.update_book(
        pk=1, values={"title": "test_book0_updated", "is_available": False}
    )
    assert res == (
        1,
        "B000",
        "test_book0_updated",
        "test_author0",
        "test_publisher0",
        False,
    )
