from dataclasses import dataclass
from uuid import UUID


@dataclass
class IngestionRun:
    id: UUID
    chunking_strategy: str
    chunking_config: dict
    embedding_config: dict
