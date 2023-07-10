import psycopg2
import setting

db = psycopg2.connect(
    host=setting.DB_URL,
    dbname=setting.DB_NAME,
    user=setting.DB_USER,
    password=setting.DB_PASSWD,
    port=setting.DB_PORT,
)
