import os
from uuid import UUID

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

OLLAMA_URL = os.getenv("OLLAMA_URL")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K"))

_raw_ingestion_run_id = os.getenv("DEFAULT_INGESTION_RUN_ID")

DEFAULT_INGESTION_RUN_ID: UUID | None = (
    UUID(_raw_ingestion_run_id) if _raw_ingestion_run_id else None
)


def require_default_ingestion_run_id():
    if DEFAULT_INGESTION_RUN_ID is None:
        raise RuntimeError(
            "DEFAULT_INGESTION_RUN_ID is not configured. "
            "Run ingestion, copy the generated UUID, and add it to .env."
        )

    return DEFAULT_INGESTION_RUN_ID
