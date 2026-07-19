import logging

from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.logging_config import setup_logging
from src.config.settings import DEFAULT_INGESTION_RUN_ID
from src.ingestion.ingester import get_ingestion_run_by_id
from src.pipeline.pipeline import answer_question

setup_logging(level=logging.DEBUG)

if __name__ == "__main__":
    with get_connection() as conn:
        with conn.cursor() as cursor:
            ingestion_run = get_ingestion_run_by_id(cursor=cursor, ingestion_run_id=DEFAULT_INGESTION_RUN_ID)

    question = "What is RAG?"
    embedded_question = embed_text(
        input_value=question,
        embedding_model=ingestion_run.embedding_config["embedding_model"]
    )[0]

    response = answer_question(
        ingestion_run=ingestion_run,
        question=question,
        embedded_question=embedded_question
    )
    print(response)
