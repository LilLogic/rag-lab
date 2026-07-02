from typing import List


class DocumentChunk:
    def __init__(self,
                 source: str,
                 content: str,
                 embedding: List[float],
                 tags: List[str],
                 chunk_index: int,
                 embedding_model: str,
                 chunk_size: int,
                 chunk_overlap: int):
        self.source = source
        self.content = content
        self.embedding = embedding
        self.tags = tags
        self.chunk_index = chunk_index
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
