from uuid import UUID

from src.evaluation.evaluator import evaluate_cases
from src.models.ingestion_run import IngestionRun
from src.models.retrieved_chunk import RetrievedChunk


def test_evaluate_cases_with_retrieved_chunks():
    top_k = 5

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

    ingestion_run = IngestionRun(
        id=UUID("0199c8cf-ccf2-40c1-934b-67f71d2ac907"),
        chunking_strategy="fixed-size",
        embedding_config={"embedding_model": "sentence-transformers/all-MiniLM-L6-v2"},
        chunking_config={"chunk_size": 100}
    )

    fake_embed_fn = lambda input_value: [1.0, 1.0, 1.0, 1.0, 1.0]

    def fake_retrieve(embedded_question, top_k):
        assert embedded_question == [1.0, 1.0, 1.0, 1.0, 1.0]
        assert top_k == 5
        return retrieved_chunks

    evaluations = evaluate_cases(
        eval_dataset=eval_dataset,
        embed_fn=fake_embed_fn,
        retrieve_fn=fake_retrieve,
        top_k=top_k
    )

    assert len(evaluations) == 1
    assert evaluations[0]["question"] == "What is the meaning of life?"
    assert evaluations[0]["retrieved_sources"] == ["42.txt"]
    assert evaluations[0]["hit_at_1"] is True
    assert evaluations[0]["reciprocal_rank"] == 1.0
    assert evaluations[0][f"precision_at_{top_k}"] == 1 / 5
    assert evaluations[0][f"recall_at_{top_k}"] == 1.0
