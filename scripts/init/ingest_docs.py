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
import uuid

from src.chunking.chunker import chunk_text
from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.logging_config import setup_logging
from src.config.paths import ROOT_DIR
from src.config.settings import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
from src.ingestion.ingester import insert_document_chunk, insert_ingestion_run, insert_chunk_embedding
from src.llm.tag_extractor import extract_tags
from src.models.document_chunk import DocumentChunk
from src.models.ingestion_run import IngestionRun

setup_logging()
logger = logging.getLogger(__name__)

DOCS_DIR = ROOT_DIR / "data/raw_docs"


def main():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            ingestion_run_id = uuid.uuid4()
            logger.info(f"Ingestion run id: {ingestion_run_id}")

            chunking_config = {
                "chunk_size": CHUNK_SIZE,
                "chunk_overlap": CHUNK_OVERLAP,
                "length_unit": "characters"
            }
            embedding_config = {
                "embedding_model": EMBEDDING_MODEL,
                "dimension": 768
            }

            ingestion_run = IngestionRun(
                id=ingestion_run_id,
                chunking_strategy="fixed-size",
                embedding_config=embedding_config,
                chunking_config=chunking_config
            )

            insert_ingestion_run(cursor, ingestion_run)

            for file_path in DOCS_DIR.glob("*.txt"):
                text = file_path.read_text(encoding="utf-8")
                tags = extract_tags(text)
                logger.info(f"Chunking {file_path.name}")

                chunks = chunk_text(
                    text=text,
                    chunk_size=CHUNK_SIZE,
                    chunk_overlap=CHUNK_OVERLAP
                )

                metadata = {}

                for e, chunk in enumerate(chunks):
                    embedding = embed_text(
                        input_value=chunk,
                        embedding_model=ingestion_run.embedding_config["embedding_model"]
                    )[0]
                    document_chunk = DocumentChunk(
                        ingestion_run_id=ingestion_run_id,
                        source=file_path.name,
                        content=chunk,
                        tags=tags,
                        metadata=metadata,
                        chunk_index=e
                    )
                    document_chunk_id = insert_document_chunk(
                        cursor=cursor,
                        chunk=document_chunk
                    )

                    insert_chunk_embedding(cursor=cursor, document_chunk_id=document_chunk_id, embedding=embedding)

    logger.info("Ingestion complete.")


if __name__ == "__main__":
    main()
