import pytest

from src.client.postgres_client import get_connection


@pytest.fixture
def db_cursor():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            try:
                yield cursor
            finally:
                connection.rollback()
