from src.client.postgres_client import get_connection
from src.config.settings import require_default_ingestion_run_id
from src.ingestion.ingester import get_ingestion_run_by_id

ingestion_run_id = require_default_ingestion_run_id()

with get_connection() as conn:
    with conn.cursor() as cursor:
        print(
            get_ingestion_run_by_id(
                cursor=cursor,
                ingestion_run_id=ingestion_run_id
            ))
