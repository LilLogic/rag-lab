from uuid import UUID

from src.models.document_chunk import DocumentChunk


def test_document_chunk():
    document_chunk = DocumentChunk(
        source="source.txt",
        content="This is a chunk of text.",
        tags=["tag1", "tag2"],
        chunk_index=0,
        metadata={},
        ingestion_run_id=UUID("0199c8cf-ccf2-40c1-934b-67f71d2ac907")
    )

    assert document_chunk.source == "source.txt"
    assert document_chunk.content == "This is a chunk of text."
    assert document_chunk.tags == ["tag1", "tag2"]
    assert document_chunk.chunk_index == 0
    assert document_chunk.metadata == {}
    assert document_chunk.ingestion_run_id == UUID("0199c8cf-ccf2-40c1-934b-67f71d2ac907")
