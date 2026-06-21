import requests

from src.config.settings import OLLAMA_URL, LLM_MODEL

def generate(prompt: str, stream: bool = False):
    response = requests.post(
        url=f"{OLLAMA_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": stream
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]
