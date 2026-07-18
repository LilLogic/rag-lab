import logging
from uuid import UUID

from psycopg.types.json import Jsonb

from src.models.document_chunk import DocumentChunk
from src.models.ingestion_run import IngestionRun

logger = logging.getLogger(__name__)


def truncate_cascade(cur):
    query = """
            TRUNCATE TABLE ingestion_runs CASCADE \
            """
    logger.info(query)
    cur.execute(query)


def insert_document_chunk(cursor, chunk: DocumentChunk):
    logger.info(f"Inserting {chunk.chunk_index=} from {chunk.source}")
    cursor.execute(
        """
        INSERT INTO document_chunks (source, content, tags, chunk_index, metadata, ingestion_run_id)
        VALUES (%s, %s, %s::TEXT[], %s, %s, %s::UUID)
        RETURNING id
        """,
        (chunk.source, chunk.content, chunk.tags, chunk.chunk_index, Jsonb(chunk.metadata), chunk.ingestion_run_id),
    )

    row = cursor.fetchone()

    if row is None:
        raise Exception("The chunk insert did not return an id")

    chunk_id = row[0]
    return chunk_id


def insert_ingestion_run(cursor, ingestion_run: IngestionRun):
    logger.info(f"Inserting ingestion run {ingestion_run.id}")
    cursor.execute(
        """
        INSERT INTO ingestion_runs (id, chunking_strategy, embedding_config, chunking_config)
        VALUES (%s::UUID, %s, %s, %s)
        """,
        (ingestion_run.id, ingestion_run.chunking_strategy, Jsonb(ingestion_run.embedding_config), Jsonb(ingestion_run.chunking_config))
    )


def insert_chunk_embedding(cursor, document_chunk_id: int, embedding: list[float]):
    logger.info(f"Inserting embedding for document_chunk_id {document_chunk_id}")
    cursor.execute(
        """
        INSERT INTO chunk_embeddings_768 (document_chunk_id, embedding)
        VALUES (%s, %s::vector)
        """,
        (document_chunk_id, embedding),
    )


def get_ingestion_run_by_id(cursor, ingestion_run_id: UUID):
    logger.info(f"Getting ingestion run by id {ingestion_run_id}")
    cursor.execute(
        """
        SELECT id, chunking_strategy, embedding_config, chunking_config 
        FROM ingestion_runs 
        WHERE id = %s::UUID
        """,
        (ingestion_run_id,)
    )
    row = cursor.fetchone()
    if row is None:
        raise Exception(f"Ingestion run with id {ingestion_run_id} not found")

    ingestion_run = IngestionRun(
        id=row[0],
        chunking_strategy=row[1],
        embedding_config=row[2],
        chunking_config=row[3]
    )

    return ingestion_run