from dataclasses import dataclass
from typing import List


@dataclass
class RetrievedChunk:
    source: str
    content: str
    distance: float
    tags: List[str]
