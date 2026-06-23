from src.retrieval.retriever import retrieve
from src.utils.logging_config import setup_logging

setup_logging()


def main():
    question = "What is Docker Compose?"

    results = retrieve(question, top_k=5)

    print(f"\nQuestion: {question}\n")

    for i, row in enumerate(results, start=1):
        source, content, distance = row

        print(f"Result {i}")
        print(f"Source: {source}")
        print(f"Distance: {distance}")
        print(f"Content: {content[:500]}")
        print("-" * 80)


if __name__ == "__main__":
    main()