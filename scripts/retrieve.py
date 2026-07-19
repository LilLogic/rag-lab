from src.client.postgres_client import get_connection
from src.config.settings import DEFAULT_INGESTION_RUN_ID
from src.ingestion.ingester import get_ingestion_run_by_id
from src.retrieval.retriever import retrieve
from src.config.logging_config import setup_logging

setup_logging()


def main():
    question = "Explain cache invalidation."

    with get_connection() as conn:
        with conn.cursor() as cursor:
            ingestion_run = get_ingestion_run_by_id(
                        cursor=cursor,
                        ingestion_run_id=DEFAULT_INGESTION_RUN_ID
                    )

    results = retrieve(
        question=question,
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


if __name__ == "__main__":
    main()
