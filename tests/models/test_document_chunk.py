from src.models.document_chunk import DocumentChunk


def test_document_chunk():
    document_chunk = DocumentChunk(
        source="source.txt",
        content="This is a chunk of text.",
        embedding=[0.1, 0.2, 0.3],
        tags=["tag1", "tag2"],
        chunk_index=0,
        embedding_model="test_model",
        chunk_size=10,
        chunk_overlap=2
    )

    assert document_chunk.source == "source.txt"
    assert document_chunk.content == "This is a chunk of text."
    assert document_chunk.embedding == [0.1, 0.2, 0.3]
    assert document_chunk.tags == ["tag1", "tag2"]
    assert document_chunk.chunk_index == 0
    assert document_chunk.embedding_model == "test_model"
    assert document_chunk.chunk_size == 10
    assert document_chunk.chunk_overlap == 2
