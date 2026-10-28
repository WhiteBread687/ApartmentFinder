"""One connection per query operation, always closed."""
from contextlib import contextmanager
from config import DB_CONFIG
@contextmanager
def connection():
    import mysql.connector
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()
