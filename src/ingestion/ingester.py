import logging

from src.models.document_chunk import DocumentChunk

logger = logging.getLogger(__name__)


def reset_table(cur):
    logger.info("Truncate table document_chunks")
    cur.execute(
        """
        TRUNCATE TABLE document_chunks RESTART IDENTITY
        """
    )


def insert_chunk(cursor, chunk: DocumentChunk):
    logger.info(f"Inserting chunk {chunk.chunk_index} from {chunk.source}")
    cursor.execute(
        """
        INSERT INTO document_chunks (source, content, embedding, tags, chunk_index, embedding_model, chunk_size, chunk_overlap)
        VALUES (%s, %s, %s::vector, %s::text[], %s, %s, %s, %s)
        """,
        (chunk.source, chunk.content, chunk.embedding, chunk.tags, chunk.chunk_index, chunk.embedding_model, chunk.chunk_size, chunk.chunk_overlap),
    )
