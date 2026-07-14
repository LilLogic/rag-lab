from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class DocumentChunk:
    source: str
    content: str
    tags: List[str]
    metadata: dict
    chunk_index: int
    ingestion_run_id: UUID
