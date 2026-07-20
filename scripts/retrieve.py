from src.client.embedding_client import embed_text
from src.client.postgres_client import get_connection
from src.config.logging_config import setup_logging
from src.config.settings import require_default_ingestion_run_id
from src.ingestion.ingester import get_ingestion_run_by_id
from src.retrieval.retriever import retrieve

setup_logging()

if __name__ == "__main__":
    question = "Explain cache invalidation."
    ingestion_run_id = require_default_ingestion_run_id()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            ingestion_run = get_ingestion_run_by_id(
                cursor=cursor,
                ingestion_run_id=ingestion_run_id
            )

    embedded_question = embed_text(input_value=question, embedding_model=ingestion_run.embedding_config["embedding_model"])[0]

    results = retrieve(
        embedded_question=embedded_question,
        ingestion_run=ingestion_run,
        top_k=5,
        tags=["caching", "expiration"]
    )

    print(f"\nQuestion: {question}\n")

    for i, chunk in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source: {chunk.source}")
        print(f"Distance: {chunk.distance}")
        print(f"Tags: {chunk.tags}")
        print(f"Content: {chunk.content[:500]}")
        print("-" * 80)
