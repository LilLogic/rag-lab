import logging

from src.client.llm_client import generate
from src.models.ingestion_run import IngestionRun
from src.retrieval.retriever import retrieve

logger = logging.getLogger(__name__)


def answer_question(ingestion_run: IngestionRun, question: str, embedded_question: list[float]):
    document_chunks = retrieve(ingestion_run=ingestion_run, embedded_question=embedded_question, top_k=5)
    logger.debug(f"document_chunks: {document_chunks}")

    prompt = f"Answer the following question only using the provided sources.\n\nQuestion: {question}\n\nSources: \n{"\n".join([chunk.content for chunk in document_chunks])}"
    logger.debug(f"prompt: {prompt}")

    response = generate(prompt)
    logger.debug(f"response: {response}")

    return response
