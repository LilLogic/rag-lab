"""
Document ingestion pipeline.

This script:
1. Loads text documents from the raw_docs directory.
2. Splits documents into chunks.
3. Generates embeddings for each chunk.
4. Stores chunks and embeddings in PostgreSQL/pgvector.

Usage:
    python ingest_docs.py
"""
import logging

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.settings import EMBEDDING_MODEL
from src.llm.tag_extractor import extract_tags
from src.models.document_chunk import DocumentChunk
from src.chunking.chunker import chunk_text, CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.logging_config import setup_logging
from src.utils.paths import ROOT_DIR

setup_logging()
logger = logging.getLogger(__name__)

DOCS_DIR = ROOT_DIR / "data/raw_docs"


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


def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            reset_table(cur)
            for file_path in DOCS_DIR.glob("*.txt"):
                text = file_path.read_text(encoding="utf-8")
                tags = extract_tags(text)
                logger.info(f"Chunking {file_path.name}")
                for e, chunk in enumerate(chunk_text(text)):
                    embedding = embed_text(chunk)[0]
                    document_chunk = DocumentChunk(
                        source=file_path.name,
                        content=chunk,
                        embedding=embedding,
                        tags=tags,
                        chunk_index=e,
                        embedding_model=EMBEDDING_MODEL,
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=CHUNK_OVERLAP
                    )
                    insert_chunk(
                        cursor=cur,
                        chunk=document_chunk
                    )

    logger.info("Ingestion complete.")


if __name__ == "__main__":
    main()
