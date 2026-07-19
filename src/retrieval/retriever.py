import logging

from src.client.postgres_client import get_connection
from src.config.settings import DEFAULT_TOP_K
from src.models.ingestion_run import IngestionRun
from src.models.retrieved_chunk import RetrievedChunk

logger = logging.getLogger(__name__)


def retrieve_with_cursor(cursor, embedded_question: list[float], ingestion_run: IngestionRun, top_k: int = DEFAULT_TOP_K,
                         tags: list[str] | None = None) -> list[RetrievedChunk]:
    logger.debug(f"Retrieving {top_k=} chunks")

    if tags:
        cursor.execute(
            """
            SELECT dc.source,
                   dc.content,
                   dc.tags,
                   ce.embedding <=> %s::vector AS distance
            FROM document_chunks dc
                     INNER JOIN chunk_embeddings_768 ce ON dc.id = ce.document_chunk_id
            WHERE dc.ingestion_run_id = %s::UUID
              AND tags && %s::text[]
            ORDER BY distance
            LIMIT %s
            """,
            (embedded_question, ingestion_run.id, tags, top_k),
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
            SELECT dc.source,
                   dc.content,
                   ce.embedding <=> %s::vector AS distance
            FROM document_chunks dc
                     INNER JOIN chunk_embeddings_768 ce ON dc.id = ce.document_chunk_id
            WHERE dc.ingestion_run_id = %s::UUID
            ORDER BY distance
            LIMIT %s
            """,
            (embedded_question, ingestion_run.id, top_k),
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


def retrieve(embedded_question: list[float], ingestion_run: IngestionRun, top_k: int = DEFAULT_TOP_K, tags: list[str] | None = None) -> list[
    RetrievedChunk]:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            return retrieve_with_cursor(
                cursor=cursor,
                embedded_question=embedded_question,
                ingestion_run=ingestion_run,
                top_k=top_k,
                tags=tags
            )
