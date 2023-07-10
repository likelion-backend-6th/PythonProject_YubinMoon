import psycopg2
import setting


def connect(func):
    def inner(*args, **kwargs):
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

    return inner


@connect
def create_tables(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            pk int GENERATED ALWAYS AS IDENTITY,
            book_id VARCHAR(20) NOT NULL,
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
            id int GENERATED ALWAYS AS IDENTITY,
            book_pk int NOT NULL,
            loan_date DATE NOT NULL,
            return_date DATE NULL,
            PRIMARY KEY(id)
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
    cur, book_id: str, title: str, author: str, publisher: str
) -> list[str]:
    sql = "INSERT INTO books (book_id, title, author, publisher) VALUES (%s, %s, %s, %s) RETURNING pk;"
    cur.execute(sql, (book_id, title, author, publisher))
    return cur.fetchone()[0]


@connect
def read_books(
    cur, limit: int = 10, offset: int = 0, order_by: str = "book_id"
) -> list[tuple[str]]:
    sql = f"SELECT * FROM books ORDER BY {order_by} LIMIT %s OFFSET %s;"
    cur.execute(sql, (limit, offset))
    return cur.fetchall()


if __name__ == "__main__":
    create_tables()