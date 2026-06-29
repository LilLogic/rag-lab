import logging

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection

logger = logging.getLogger(__name__)

TOP_K = 5


def retrieve_with_cursor(cursor, question: str, top_k: int = TOP_K):
    logger.debug(f"Retrieving top {top_k} chunks for question: {question}")

    embedded_question = embed_text(question)[0]

    cursor.execute(
        """
        SELECT source,
               content,
               embedding <=> %s::vector AS distance
        FROM document_chunks
        ORDER BY distance ASC
        LIMIT %s
        """,
        (embedded_question, top_k),
    )

    return cursor.fetchall()


def retrieve(question: str, top_k: int = TOP_K):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            return retrieve_with_cursor(cursor, question, top_k)
