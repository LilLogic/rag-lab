from dataclasses import dataclass
from typing import List

@dataclass
class DocumentChunk:
     source: str
     content: str
     embedding: List[float]
     tags: List[str]
     chunk_index: int
     embedding_model: str
     chunk_size: int
     chunk_overlap: int
