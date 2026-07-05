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

from src.chunking.chunker import chunk_text
from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.logging_config import setup_logging
from src.config.paths import ROOT_DIR
from src.config.settings import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
from src.ingestion.ingester import reset_table, insert_chunk
from src.llm.tag_extractor import extract_tags
from src.models.document_chunk import DocumentChunk

setup_logging()
logger = logging.getLogger(__name__)

DOCS_DIR = ROOT_DIR / "data/raw_docs"


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
