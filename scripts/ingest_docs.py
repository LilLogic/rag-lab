"""
Document ingestion pipeline.

This script:
1. Loads text documents from the docs directory.
2. Splits documents into chunks.
3. Generates embeddings for each chunk.
4. Stores chunks and embeddings in PostgreSQL/pgvector.

Usage:
    python ingest_docs.py
"""

from pathlib import Path

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection

DOCS_DIR = Path("../data/docs")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def reset_table(cur):
    print("Truncate table document_chunks")
    cur.execute(
        """
        TRUNCATE TABLE document_chunks RESTART IDENTITY
        """
    )


def insert_chunk(cursor, source: str, content: str, embedding: list):
    cursor.execute(
        """
        INSERT INTO document_chunks (source, content, embedding)
        VALUES (%s, %s, %s)
        """,
        (source, content, embedding),
    )


def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            reset_table(cur)
            for file_path in DOCS_DIR.glob("*.txt"):
                text = file_path.read_text(encoding="utf-8")
                print(f"Chunking {file_path.name}")
                for chunk in chunk_text(text):
                    embedding = embed_text(chunk)[0]
                    insert_chunk(cur, file_path.name, chunk, embedding)

    print("Ingestion complete.")


if __name__ == "__main__":
    main()
