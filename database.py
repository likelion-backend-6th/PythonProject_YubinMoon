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
def create_db(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id int GENERATED ALWAYS AS IDENTITY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(50) NOT NULL,
            publisher VARCHAR(50) NOT NULL,
            is_available BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY(id)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS loans (
            id int GENERATED ALWAYS AS IDENTITY,
            book_id int NOT NULL,
            loan_date DATE NOT NULL,
            return_date DATE NULL
        );
        """
    )


@connect
def get_db(cur) -> str:
    cur.execute(
        """
        SELECT current_database();
        """
    )
    return cur.fetchone()


@connect
def add_book(cur, title: str, author: str, publisher: str) -> None:
    cur.execute(
        """
        INSERT INTO books (title, author, publisher) VALUES (%s, %s, %s);
        """,
        (title, author, publisher),
    )


if __name__ == "__main__":
    create_db()
