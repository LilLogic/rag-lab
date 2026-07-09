from src.config.logging_config import setup_logging
from src.pipeline.pipeline import answer_question

setup_logging()

question = "What is RAG?"

response = answer_question(question)

print(response)
