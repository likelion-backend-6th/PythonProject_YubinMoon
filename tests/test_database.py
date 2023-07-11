from pprint import pprint
import psycopg2
import pytest
from unittest.mock import patch
import setting
import datetime

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


def test_read_books_by_book_id():
    res = database.count_books_by_book_id("B001")
    assert res == 1
    res = database.count_books_by_book_id("00")
    assert res == 10

    res = database.read_books_by_Book_id("B001")
    assert res == [(2, "B001", "test_book1", "test_author1", "test_publisher1", True)]
    res = database.read_books_by_Book_id("00")
    assert len(res) == 10


def test_read_books_by_book_title():
    res = database.count_books_by_title("book1")
    assert res == 1
    res = database.count_books_by_title("book")
    assert res == 10

    res = database.read_books_by_Book_id("B001")
    assert res == [(2, "B001", "test_book1", "test_author1", "test_publisher1", True)]
    res = database.read_books_by_Book_id("00")
    assert len(res) == 10


def test_read_book_by_pk():
    res = database.read_book_by_pk(1)
    assert res == (1, "B000", "test_book0", "test_author0", "test_publisher0", True)


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


def test_add_loan():
    for i in range(10):
        res = database.create_loan(book_pk=i + 1, loan_date=datetime.datetime.today())
        assert res == i + 1


def test_read_loans():
    res = database.read_loans()
    for idx, data in enumerate(res):
        assert data[0] == idx + 1
        assert data[1] == idx + 1
        assert data[2] == datetime.datetime.now().date()
        assert data[3] is None

    res = database.read_loans(limit=3, offset=2, order_by="loan_date")
    for idx, data in enumerate(res):
        assert data[0] == idx + 3
        assert data[1] == idx + 3
        assert data[2] == datetime.datetime.now().date()
        assert data[3] is None


def test_read_loans_by_book_pk():
    res = database.read_loans_by_book_pk(1)
    assert res == [(1, 1, datetime.datetime.now().date(), None)]


def test_read_loan_return_null():
    res = database.read_loan_return_null(1)
    assert res == (1, 1, datetime.datetime.now().date(), None)

    res = database.read_loan_return_null(100)
    assert res is None


def test_update_loan():
    res = database.update_loan(
        pk=1, values={"return_date": datetime.datetime.now().date()}
    )
    assert res == (1, 1, datetime.datetime.now().date(), datetime.datetime.now().date())


def test_count_book():
    res = database.count_books()
    assert res == 10


def test_loan_count_by_book_pk():
    res = database.loan_count_by_book_pk(1)
    assert res == 1


def test_all_loan_history():
    res = database.all_loan_history()
    assert len(res) == 10
