import json
import logging
from dataclasses import asdict

from src.client.postgres_client import get_connection
from src.config.paths import ROOT_DIR
from src.config.settings import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
from src.evaluation.metrics import reciprocal_rank, precision_at_top_k, recall_at_top_k, hit_at_k
from src.evaluation.report_writer import create_eval_run_dir, save_json
from src.models.retrieved_chunk import RetrievedChunk
from src.retrieval.retriever import retrieve_with_cursor

logger = logging.getLogger(__name__)

TOP_K = 5


def evaluate_case(case: dict, retrieved_chunks: list[RetrievedChunk], top_k: int) -> dict:
    question = case["question"]
    expected_sources = set(case["expected_sources"])

    retrieved_sources = [chunk.source for chunk in retrieved_chunks]

    return {
        "question": question,
        "expected_sources": expected_sources,
        "retrieved_sources": retrieved_sources,
        "results": [asdict(chunk) for chunk in retrieved_chunks],

        "hit_at_1": hit_at_k(retrieved_sources, expected_sources, k=1),
        "hit_at_3": hit_at_k(retrieved_sources, expected_sources, k=3),
        f"hit_at_{top_k}": hit_at_k(retrieved_sources, expected_sources, k=top_k),

        "reciprocal_rank": reciprocal_rank(retrieved_sources, expected_sources),
        f"precision_at_{top_k}": precision_at_top_k(retrieved_sources, expected_sources, k=top_k),
        f"recall_at_{top_k}": recall_at_top_k(retrieved_sources, expected_sources, k=top_k),
    }


def evaluate_cases(eval_dataset: list[dict], retrieve_fn, top_k) -> list[dict]:
    evaluations = []

    for i, case in enumerate(eval_dataset):
        logger.info(f"Evaluating case {i + 1}/{len(eval_dataset)}: {case['question']}")

        retrieved_chunks = retrieve_fn(case["question"], top_k)
        evaluations.append(
            evaluate_case(
                case=case,
                retrieved_chunks=retrieved_chunks,
                top_k=top_k
            )
        )

    return evaluations


def evaluate(top_k: int = TOP_K):
    run_dir = create_eval_run_dir()

    eval_dataset_path = "data/evaluation/eval_dataset.json"
    with open(ROOT_DIR / eval_dataset_path, "r") as f:
        eval_dataset = json.load(f)

    config = {
        "top_k": top_k,
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

    evaluations = []
    with get_connection() as conn:
        with conn.cursor() as cursor:
            evaluations = evaluate_cases(
                eval_dataset=eval_dataset,
                retrieve_fn=lambda question, top_k: retrieve_with_cursor(cursor, question, top_k),
                top_k=top_k
            )

    total_questions = len(evaluations)
    mean_hit_at_1 = sum(e["hit_at_1"] for e in evaluations) / total_questions
    mean_hit_at_3 = sum(e["hit_at_3"] for e in evaluations) / total_questions
    mean_hit_at_top_k = sum(e[f"hit_at_{top_k}"] for e in evaluations) / total_questions
    mean_reciprocal_rank = sum(e["reciprocal_rank"] for e in evaluations) / total_questions
    mean_precision_at_top_k = sum(e[f"precision_at_{top_k}"] for e in evaluations) / total_questions
    mean_recall_at_top_k = sum(e[f"recall_at_{top_k}"] for e in evaluations) / total_questions

    summary = {
        "total_questions": total_questions,
        "mean_hit_at_1": mean_hit_at_1,
        "mean_hit_at_3": mean_hit_at_3,
        f"mean_hit_at_{top_k}": mean_hit_at_top_k,
        "mean_reciprocal_rank": mean_reciprocal_rank,
        f"mean_precision_at_{top_k}": mean_precision_at_top_k,
        f"mean_recall_at_{top_k}": mean_recall_at_top_k
    }
    save_json(path=run_dir / "summary.json", data=summary)

    print("\nRETRIEVAL EVALUATION")
    print(f"Total questions: {total_questions}")
    print(f"Mean Hit@1: {mean_hit_at_1:.2f}")
    print(f"Mean Hit@3: {mean_hit_at_3:.2f}")
    print(f"Mean Hit@{top_k}: {mean_hit_at_top_k:.2f}")
    print(f"Mean Reciprocal Rank: {mean_reciprocal_rank:.2f}")
    print(f"Mean Precision@{top_k}: {mean_precision_at_top_k:.2f}")
    print(f"Mean Recall@{top_k}: {mean_recall_at_top_k:.2f}")

    details = list()
    for e in evaluations:
        details.append({
            "question": e["question"],
            "expected_sources": sorted(e["expected_sources"]),
            "retrieved_sources": e["retrieved_sources"],
            "results": e["results"],
            "hit_at_1": e["hit_at_1"],
            "hit_at_3": e["hit_at_3"],
            f"hit_at_{top_k}": e[f"hit_at_{top_k}"],
            "reciprocal_rank": e["reciprocal_rank"],
            f"precision_at_{top_k}": e[f"precision_at_{top_k}"],
            f"recall_at_{top_k}": e[f"recall_at_{top_k}"]
        })

        print("\n" + "=" * 80)
        print(f"Question: {e['question']}")
        print(f"Expected: {sorted(e['expected_sources'])}")
        print(f"Retrieved: {e['retrieved_sources']}")
        print(f"Hit@1: {e['hit_at_1']} | Hit@3: {e['hit_at_3']} | Hit@{top_k}: {e[f'hit_at_{top_k}']}")

        for rank, row in enumerate(e["results"], start=1):
            print(f"{rank}. {row["source"]} | distance={row["distance"]:.4f}")

    save_json(path=run_dir / "details.json", data=details)
