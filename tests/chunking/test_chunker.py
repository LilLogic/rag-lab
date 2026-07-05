from src.chunking.chunker import chunk_text


def test_chunk_text_returns_expected_chunks():
    text = "abcdefghij"

    chunks = chunk_text(text, chunk_size=4, chunk_overlap=1)

    assert chunks == ["abcd", "defg", "ghij", "j"]


def test_chunk_text_shorter_than_chunk_size():
    text = "abc"

    chunks = chunk_text(text, chunk_size=10, chunk_overlap=2)

    assert chunks == ["abc"]
