from src.evaluation.metrics import (
    hit_at_k,
    precision_at_top_k,
    recall_at_top_k,
    reciprocal_rank,
)


def test_hit_at_k_returns_true_when_expected_source_is_in_top_k():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "A.txt", "C.txt"]

    assert hit_at_k(retrieved_sources, expected_sources, k=2) is True


def test_hit_at_k_returns_false_when_expected_source_is_outside_top_k():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "C.txt", "A.txt"]

    assert hit_at_k(retrieved_sources, expected_sources, k=2) is False


def test_hit_at_k_returns_false_when_no_source_matches():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "C.txt", "D.txt"]

    assert hit_at_k(retrieved_sources, expected_sources, k=3) is False


def test_hit_at_k_handles_multiple_expected_sources():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["C.txt", "B.txt", "D.txt"]

    assert hit_at_k(retrieved_sources, expected_sources, k=2) is True


def test_reciprocal_rank_returns_one_when_first_result_matches():
    expected_sources = {"A.txt"}
    retrieved_sources = ["A.txt", "B.txt", "C.txt"]

    assert reciprocal_rank(retrieved_sources, expected_sources) == 1.0


def test_reciprocal_rank_returns_inverse_rank_of_first_match():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "C.txt", "A.txt"]

    assert reciprocal_rank(retrieved_sources, expected_sources) == 1 / 3


def test_reciprocal_rank_uses_first_matching_expected_source():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["C.txt", "B.txt", "A.txt"]

    assert reciprocal_rank(retrieved_sources, expected_sources) == 1 / 2


def test_reciprocal_rank_returns_zero_when_no_match():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "C.txt"]

    assert reciprocal_rank(retrieved_sources, expected_sources) == 0.0


def test_precision_at_k_counts_relevant_sources_in_top_k():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["A.txt", "C.txt", "B.txt", "D.txt"]

    assert precision_at_top_k(retrieved_sources, expected_sources, k=4) == 0.5


def test_precision_at_k_uses_only_top_k_results():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["A.txt", "C.txt", "D.txt", "B.txt"]

    assert precision_at_top_k(retrieved_sources, expected_sources, k=3) == 1 / 3


def test_precision_at_k_returns_zero_when_no_relevant_sources_in_top_k():
    expected_sources = {"A.txt"}
    retrieved_sources = ["B.txt", "C.txt"]

    assert precision_at_top_k(retrieved_sources, expected_sources, k=2) == 0.0


def test_recall_at_k_counts_fraction_of_expected_sources_found():
    expected_sources = {"A.txt", "B.txt", "C.txt"}
    retrieved_sources = ["A.txt", "D.txt", "B.txt"]

    assert recall_at_top_k(retrieved_sources, expected_sources, k=3) == 2 / 3


def test_recall_at_k_uses_only_top_k_results():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["A.txt", "C.txt", "B.txt"]

    assert recall_at_top_k(retrieved_sources, expected_sources, k=2) == 0.5


def test_recall_at_k_returns_zero_when_no_expected_sources_found():
    expected_sources = {"A.txt", "B.txt"}
    retrieved_sources = ["C.txt", "D.txt"]

    assert recall_at_top_k(retrieved_sources, expected_sources, k=2) == 0.0
