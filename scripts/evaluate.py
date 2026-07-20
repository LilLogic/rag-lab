from src.client.postgres_client import get_connection
from src.config.logging_config import setup_logging
from src.config.settings import DEFAULT_TOP_K, require_default_ingestion_run_id
from src.evaluation.evaluator import evaluate
from src.ingestion.ingester import get_ingestion_run_by_id

setup_logging()

if __name__ == "__main__":
    ingestion_run_id = require_default_ingestion_run_id()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            ingestion_run = get_ingestion_run_by_id(
                cursor=cursor,
                ingestion_run_id=ingestion_run_id
            )
    evaluate(
        ingestion_run=ingestion_run,
        top_k=DEFAULT_TOP_K
    )
