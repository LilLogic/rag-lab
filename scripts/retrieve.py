from src.retrieval.retriever import retrieve
from src.config.logging_config import setup_logging

setup_logging()


def main():
    question = "Explain cache invalidation."

    results = retrieve(question, top_k=5, tags=["caching", "expiration"])

    print(f"\nQuestion: {question}\n")

    for i, chunk in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source: {chunk.source}")
        print(f"Distance: {chunk.distance}")
        print(f"Tags: {chunk.tags}")
        print(f"Content: {chunk.content[:500]}")
        print("-" * 80)


if __name__ == "__main__":
    main()
