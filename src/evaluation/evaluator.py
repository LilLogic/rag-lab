import json
import logging

from src.client.postgres_client import get_connection
from src.retrieval.retriever import retrieve_with_cursor
from src.utils.paths import ROOT_DIR

logger = logging.getLogger(__name__)

TOP_K = 5


def reciprocal_rank(retrieved_sources, expected_sources):
    for rank, source in enumerate(retrieved_sources, start=1):
        if source in expected_sources:
            return 1 / rank
    return 0.0


def precision_at_k(retrieved_sources, expected_sources, k):
    retrieved_k = retrieved_sources[:k]
    hits = sum(1 for source in retrieved_k if source in expected_sources)
    return hits / k


def recall_at_k(retrieved_sources, expected_sources, k):
    retrieved_k = retrieved_sources[:k]
    hits = len(set(retrieved_k).intersection(expected_sources))
    return hits / len(expected_sources)


def evaluate_case(cursor, case):
    question = case["question"]
    expected_sources = set(case["expected_sources"])

    results = retrieve_with_cursor(cursor, question, TOP_K)
    retrieved_sources = [row[0] for row in results]

    return {
        "question": question,
        "expected_sources": expected_sources,
        "retrieved_sources": retrieved_sources,
        "results": results,

        "hit_at_1": bool(expected_sources.intersection(retrieved_sources[:1])),
        "hit_at_3": bool(expected_sources.intersection(retrieved_sources[:3])),
        "hit_at_5": bool(expected_sources.intersection(retrieved_sources[:5])),

        "mrr": reciprocal_rank(retrieved_sources, expected_sources),
        "precision_at_5": precision_at_k(retrieved_sources, expected_sources, 5),
        "recall_at_5": recall_at_k(retrieved_sources, expected_sources, 5),
    }


def evaluate():
    with open(ROOT_DIR / "data/evaluation/eval_dataset.json", "r") as f:
        eval_dataset = json.load(f)

    evaluations = []

    with get_connection() as conn:
        with conn.cursor() as cursor:
            for i, case in enumerate(eval_dataset):
                logger.info(f"Evaluating case {i + 1}/{len(eval_dataset)}: {case['question']}")
                evaluations.append(evaluate_case(cursor, case=case))

    total = len(evaluations)

    hit_at_1 = sum(e["hit_at_1"] for e in evaluations) / total
    hit_at_3 = sum(e["hit_at_3"] for e in evaluations) / total
    hit_at_5 = sum(e["hit_at_5"] for e in evaluations) / total

    print("\nRETRIEVAL EVALUATION")
    print(f"Total questions: {total}")
    print(f"Hit@1: {hit_at_1:.2f}")
    print(f"Hit@3: {hit_at_3:.2f}")
    print(f"Hit@5: {hit_at_5:.2f}")

    mrr = sum(e["mrr"] for e in evaluations) / total
    precision_at_5 = sum(e["precision_at_5"] for e in evaluations) / total
    recall_at_5 = sum(e["recall_at_5"] for e in evaluations) / total

    print(f"MRR: {mrr:.2f}")
    print(f"Precision@5: {precision_at_5:.2f}")
    print(f"Recall@5: {recall_at_5:.2f}")

    for e in evaluations:
        print("\n" + "=" * 80)
        print(f"Question: {e['question']}")
        print(f"Expected: {list(e['expected_sources'])}")
        print(f"Retrieved: {e['retrieved_sources']}")
        print(f"Hit@1: {e['hit_at_1']} | Hit@3: {e['hit_at_3']} | Hit@5: {e['hit_at_5']}")

        for rank, row in enumerate(e["results"], start=1):
            print(f"{rank}. {row[0]} | distance={row[2]:.4f}")
