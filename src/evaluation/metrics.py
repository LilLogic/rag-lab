def reciprocal_rank(retrieved_sources: list, expected_sources: set):
    for rank, source in enumerate(retrieved_sources, start=1):
        if source in expected_sources:
            return 1 / rank
    return 0.0


def precision_at_top_k(retrieved_sources: list, expected_sources: set, k):
    retrieved_k = retrieved_sources[:k]
    hits = sum(1 for source in retrieved_k if source in expected_sources)
    return hits / k


def recall_at_top_k(retrieved_sources: list, expected_sources: set, k):
    retrieved_k = retrieved_sources[:k]
    hits = len(set(retrieved_k).intersection(expected_sources))
    return hits / len(expected_sources)


def hit_at_k(retrieved_sources: list, expected_sources: set, k: int):
    return bool(expected_sources.intersection(retrieved_sources[:k]))
