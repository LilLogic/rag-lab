from src.evaluation.evaluator import evaluate_cases
from src.models.retrieved_chunk import RetrievedChunk


def test_evaluate_cases_with_retrieved_chunks():
    eval_dataset = [
        {
            "question": "What is the meaning of life?",
            "expected_sources": ["42.txt"]
        }
    ]

    retrieved_chunks = [
        RetrievedChunk(
            source="42.txt",
            content="The meaning of life is 42.",
            tags=["fish", "factorio"],
            distance=0.42
        )
    ]

    def fake_retrieve(question, top_k):
        return retrieved_chunks

    evaluations = evaluate_cases(
        eval_dataset=eval_dataset,
        retrieve_fn=fake_retrieve,
        top_k=5
    )

    assert len(evaluations) == 1
    assert evaluations[0]["question"] == "What is the meaning of life?"
    assert evaluations[0]["retrieved_sources"] == ["42.txt"]
    assert evaluations[0]["hit_at_1"] is True
    assert evaluations[0]["reciprocal_rank"] == 1.0
    assert evaluations[0]["precision_at_top_k"] == 1 / 5
    assert evaluations[0]["recall_at_top_k"] == 1.0
