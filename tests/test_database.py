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
            f"B00{i}", "test_book", "test_author", "test_publisher"
        )
        assert res == i + 1
