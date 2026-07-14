import logging

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.settings import DEFAULT_TOP_K, EMBEDDING_MODEL
from src.models.retrieved_chunk import RetrievedChunk

logger = logging.getLogger(__name__)


def retrieve_with_cursor(cursor, question: str, top_k: int = DEFAULT_TOP_K, tags: list[str] | None = None) -> list[RetrievedChunk]:
    logger.debug(f"Retrieving top {top_k} chunks for question: {question}")

    embedded_question = embed_text(
        input_value=question,
        embedding_model=EMBEDDING_MODEL
    )[0]

    if tags:
        cursor.execute(
            """
            SELECT source,
                   content,
                   tags,
                   embedding <=> %s::vector AS distance
            FROM document_chunks
            WHERE tags && %s::text[]
            ORDER BY distance
            LIMIT %s
            """,
            (embedded_question, tags, top_k),
        )
        rows = cursor.fetchall()

        return [
            RetrievedChunk(
                source=row[0],
                content=row[1],
                tags=row[2],
                distance=row[3],
            ) for row in rows
        ]
    else:
        cursor.execute(
            """
            SELECT source,
                   content,
                   embedding <=> %s::vector AS distance
            FROM document_chunks
            ORDER BY distance
            LIMIT %s
            """,
            (embedded_question, top_k),
        )
        rows = cursor.fetchall()
        return [
            RetrievedChunk(
                source=row[0],
                content=row[1],
                tags=[],
                distance=row[2],
            ) for row in rows
        ]


def retrieve(question: str, top_k: int, tags: list[str] | None = None) -> list[RetrievedChunk]:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            return retrieve_with_cursor(cursor, question, top_k, tags)
