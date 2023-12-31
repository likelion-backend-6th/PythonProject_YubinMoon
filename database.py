import psycopg2
import setting
import datetime


def connect(func):
    def inner(*args, **kwargs):
        try:
            conn = psycopg2.connect(
                host=setting.DB_URL,
                dbname=setting.DB_NAME,
                user=setting.DB_USER,
                password=setting.DB_PASSWD,
                port=setting.DB_PORT,
            )
            cur = conn.cursor()
            result = func(cur, *args, **kwargs)
            conn.commit()
            cur.close()
            return result
        except psycopg2.Error as e:
            print("DB 연결에 실패했습니다.")
            print(e)
            exit(1)

    return inner


@connect
def create_tables(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            pk int GENERATED ALWAYS AS IDENTITY,
            book_id VARCHAR(20) UNIQUE NOT NULL,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(50) NOT NULL,
            publisher VARCHAR(50) NOT NULL,
            is_available BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY(pk)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS loans (
            pk int GENERATED ALWAYS AS IDENTITY,
            book_pk int NOT NULL,
            loan_date DATE NOT NULL,
            return_date DATE NULL,
            PRIMARY KEY(pk)
        );
        """
    )


@connect
def get_db_name(cur) -> str:
    cur.execute(
        """
        SELECT current_database();
        """
    )
    return cur.fetchone()


@connect
def create_book(
    cur,
    book_id: str,
    title: str,
    author: str,
    publisher: str,
    is_available: bool = True,
) -> int:
    sql = "INSERT INTO books (book_id, title, author, publisher, is_available) VALUES (%s, %s, %s, %s, %s) RETURNING pk;"
    cur.execute(sql, (book_id, title, author, publisher, is_available))
    return cur.fetchone()[0]


@connect
def count_books(cur) -> int:
    cur.execute("SELECT COUNT(*) FROM books;")
    return cur.fetchone()[0]


@connect
def read_books(
    cur, limit: int = 10, offset: int = 0, order_by: str = "book_id"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM books ORDER BY {order_by} LIMIT %s OFFSET %s;"
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


@connect
def count_books_by_book_id(cur, book_id: str) -> int:
    sql = f"SELECT COUNT(*) FROM books WHERE book_id LIKE '%{book_id}%';"
    cur.execute(sql)
    return cur.fetchone()[0]


@connect
def read_books_by_Book_id(
    cur, book_id: str, limit: int = 10, offset: int = 0, order_by: str = "book_id"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM books WHERE book_id LIKE '%%{book_id}%%' ORDER BY {order_by} LIMIT %s OFFSET %s;"
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


@connect
def count_books_by_title(cur, title: int) -> int:
    sql = f"SELECT COUNT(*) FROM books WHERE title LIKE '%{title}%';"
    cur.execute(sql)
    return cur.fetchone()[0]


@connect
def read_books_by_title(
    cur, title: str, limit: int = 10, offset: int = 0, order_by: str = "book_id"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM books WHERE title LIKE '%%{title}%%' ORDER BY {order_by} LIMIT %s OFFSET %s;"
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


@connect
def read_book_by_pk(cur, pk: int):
    sql = "SELECT * FROM books WHERE pk = %s;"
    cur.execute(sql, (pk,))
    return cur.fetchone()


@connect
def update_book(cur, pk: int, values: dict[str, str]) -> tuple[str]:
    sql = "UPDATE books SET "
    for key, value in values.items():
        sql += f"{key} = '{value}', "
    sql = sql[:-2]
    sql += f"WHERE pk = {pk} "
    sql += "RETURNING *;"
    cur.execute(sql)
    return cur.fetchone()


@connect
def loan_count_by_book_pk(cur, book_pk: int) -> int:
    sql = f"SELECT COUNT(*) FROM loans WHERE book_pk = %s;"
    cur.execute(sql, (book_pk,))
    return cur.fetchone()[0]


@connect
def create_loan(cur, book_pk: int, loan_date: datetime.date) -> int:
    sql = "INSERT INTO loans (book_pk, loan_date) VALUES (%s, %s) RETURNING pk;"
    cur.execute(sql, (book_pk, loan_date))
    return cur.fetchone()[0]


@connect
def read_loans(
    cur, limit: int = 10, offset: int = 0, order_by: str = "loan_date"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM loans ORDER BY {order_by} LIMIT %s OFFSET %s;"
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


@connect
def read_loans_by_book_pk(
    cur, book_pk: int, limit: int = 10, offset: int = 0, order_by: str = "loan_date"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM loans WHERE book_pk = %s ORDER BY {order_by} DESC, pk DESC LIMIT %s OFFSET %s;"
    cur.execute(sql, (book_pk, limit, offset))
    return cur.fetchall()


@connect
def read_loan_return_null(cur, book_pk: int) -> list[tuple[str]]:
    sql = f"SELECT * FROM loans WHERE book_pk = %s AND return_date IS NULL;"
    cur.execute(sql, (book_pk,))
    return cur.fetchone()


@connect
def update_loan(cur, pk: int, values: dict[str, str]) -> tuple[str]:
    sql = "UPDATE loans SET "
    for key, value in values.items():
        sql += f"{key} = '{value}', "
    sql = sql[:-2]
    sql += f"WHERE pk = {pk} "
    sql += "RETURNING *;"
    cur.execute(sql)
    return cur.fetchone()


@connect
def execute_sql(cur, sql: str, values) -> list[tuple[str]]:
    cur.execute(sql, values)
    return cur.fetchall()


@connect
def all_loan_history(cur, limit: int = 10, offset: int = 0):
    sql = """SELECT b.book_id, b.title, b.author, b.publisher, l.loan_date, l.return_date 
    FROM books b 
    INNER JOIN loans l ON b.pk = l.book_pk 
    ORDER BY l.loan_date DESC, l.pk DESC 
    LIMIT %s OFFSET %s;"""
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


@connect
def all_history_count(cur) -> int:
    sql = """SELECT COUNT(*) FROM books b INNER JOIN loans l ON b.pk = l.book_pk;"""
    cur.execute(sql)
    return cur.fetchone()[0]


if __name__ == "__main__":
    create_tables()
