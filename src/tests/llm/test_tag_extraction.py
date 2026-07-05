from src.llm.tag_extractor import parse_tags


def test_parse_tags():
    document_text = "cache invalidation, expiration, consistency, write-through caching, event-driven"

    tags = parse_tags(document_text)

    assert tags == [
        "cache invalidation",
        "expiration",
        "consistency",
        "write-through caching",
        "event-driven",
    ]
