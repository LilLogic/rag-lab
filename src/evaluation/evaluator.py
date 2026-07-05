import json
import logging
from dataclasses import asdict

from src.chunking.chunker import CHUNK_SIZE, CHUNK_OVERLAP
from src.client.postgres_client import get_connection
from src.config.paths import ROOT_DIR
from src.config.settings import EMBEDDING_MODEL
from src.evaluation.metrics import reciprocal_rank, precision_at_k, recall_at_k, hit_at_k
from src.evaluation.report_writer import create_eval_run_dir, save_json
from src.retrieval.retriever import retrieve_with_cursor

logger = logging.getLogger(__name__)

TOP_K = 5


def evaluate_case(cursor, case):
    question = case["question"]
    expected_sources = set(case["expected_sources"])

    results = retrieve_with_cursor(cursor, question, TOP_K)
    retrieved_sources = [chunk.source for chunk in results]

    return {
        "question": question,
        "expected_sources": expected_sources,
        "retrieved_sources": retrieved_sources,
        "results": [asdict(chunk) for chunk in results],

        "hit_at_1": hit_at_k(retrieved_sources, expected_sources, 1),
        "hit_at_3": hit_at_k(retrieved_sources, expected_sources, 3),
        "hit_at_5": hit_at_k(retrieved_sources, expected_sources, 5),

        "reciprocal_rank": reciprocal_rank(retrieved_sources, expected_sources),
        "precision_at_5": precision_at_k(retrieved_sources, expected_sources, 5),
        "recall_at_5": recall_at_k(retrieved_sources, expected_sources, 5),
    }


def evaluate():
    run_dir = create_eval_run_dir()

    eval_dataset_path = "data/evaluation/eval_dataset.json"
    config = {
        "top_k": TOP_K,
        "eval_dataset_path": eval_dataset_path,
        "reports_path": "reports/evaluation",
        "retrieval_method": "pgvector_cosine_distance",
        "embedding_model": EMBEDDING_MODEL,
        "chunking": {
            "strategy": "fixed_size",
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        }
    }

    save_json(path=run_dir / "config.json", data=config)

    with open(ROOT_DIR / eval_dataset_path, "r") as f:
        eval_dataset = json.load(f)

    evaluations = []

    with get_connection() as conn:
        with conn.cursor() as cursor:
            for i, case in enumerate(eval_dataset):
                logger.info(f"Evaluating case {i + 1}/{len(eval_dataset)}: {case['question']}")
                evaluations.append(evaluate_case(cursor, case=case))

    total_questions = len(evaluations)
    mean_hit_at_1 = sum(e["hit_at_1"] for e in evaluations) / total_questions
    mean_hit_at_3 = sum(e["hit_at_3"] for e in evaluations) / total_questions
    mean_hit_at_5 = sum(e["hit_at_5"] for e in evaluations) / total_questions
    mean_reciprocal_rank = sum(e["reciprocal_rank"] for e in evaluations) / total_questions
    mean_precision_at_5 = sum(e["precision_at_5"] for e in evaluations) / total_questions
    mean_recall_at_5 = sum(e["recall_at_5"] for e in evaluations) / total_questions

    summary = {
        "total_questions": total_questions,
        "mean_hit_at_1": mean_hit_at_1,
        "mean_hit_at_3": mean_hit_at_3,
        "mean_hit_at_5": mean_hit_at_5,
        "mean_reciprocal_rank": mean_reciprocal_rank,
        "mean_precision_at_5": mean_precision_at_5,
        "mean_recall_at_5": mean_recall_at_5
    }

    save_json(path=run_dir / "summary.json", data=summary)

    print("\nRETRIEVAL EVALUATION")
    print(f"Total questions: {total_questions}")
    print(f"Mean Hit@1: {mean_hit_at_1:.2f}")
    print(f"Mean Hit@3: {mean_hit_at_3:.2f}")
    print(f"Mean Hit@5: {mean_hit_at_5:.2f}")
    print(f"Mean Reciprocal Rank: {mean_reciprocal_rank:.2f}")
    print(f"Mean Precision@5: {mean_precision_at_5:.2f}")
    print(f"Mean Recall@5: {mean_recall_at_5:.2f}")

    details = list()

    for e in evaluations:
        details.append({
            "question": e["question"],
            "expected_sources": sorted(e["expected_sources"]),
            "retrieved_sources": e["retrieved_sources"],
            "results": e["results"],
            "hit_at_1": e["hit_at_1"],
            "hit_at_3": e["hit_at_3"],
            "hit_at_5": e["hit_at_5"],
            "reciprocal_rank": e["reciprocal_rank"],
            "precision_at_5": e["precision_at_5"],
            "recall_at_5": e["recall_at_5"]
        })

        print("\n" + "=" * 80)
        print(f"Question: {e['question']}")
        print(f"Expected: {sorted(e['expected_sources'])}")
        print(f"Retrieved: {e['retrieved_sources']}")
        print(f"Hit@1: {e['hit_at_1']} | Hit@3: {e['hit_at_3']} | Hit@5: {e['hit_at_5']}")

        for rank, row in enumerate(e["results"], start=1):
            print(f"{rank}. {row["source"]} | distance={row["distance"]:.4f}")

    save_json(path=run_dir / "details.json", data=details)
