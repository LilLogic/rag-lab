import requests

from src.config.settings import (
    OLLAMA_URL,
    EMBEDDING_MODEL
)


def embed_text(input_value: str | list, embedding_model: str) -> list[list[float]]:
    response = requests.post(
        url=f"{OLLAMA_URL}/api/embed",
        json={
            "model": embedding_model,
            "input": input_value
        },
        timeout=60
    )
    response.raise_for_status()

    data = response.json()
    return data["embeddings"]
