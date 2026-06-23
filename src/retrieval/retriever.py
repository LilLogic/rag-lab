import logging

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection

logger = logging.getLogger(__name__)


def retrieve(question: str, top_k: int = 5):
    logger.info("Retrieving top %s chunks", top_k)

    embedded_question = embed_text(question)[0]

    with get_connection() as conn:
        with conn.cursor() as cursor:
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
