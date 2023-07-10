import psycopg2
import pytest
from unittest.mock import patch
import setting

setting.DB_NAME = "test_library"
import database


def test_create_db():
    database.create_db()
    assert "test_library" in database.get_db()


def test_add_book():
    database.add_book
