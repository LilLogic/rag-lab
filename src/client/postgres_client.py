from contextlib import contextmanager

import psycopg

from src.config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

DB_CONFIG = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD
}


@contextmanager
def get_connection():
    conn = psycopg.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
