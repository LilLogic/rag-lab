import logging

from src.client.llm_client import generate
from src.retrieval.retriever import retrieve

logger = logging.getLogger(__name__)


def answer_question(question: str):
    document_chunks = retrieve(question, top_k=5)
    logger.debug(f"document_chunks: {document_chunks}")

    prompt = f"Answer the following question only using the provided sources.\n\nQuestion: {question}\n\nSources: \n{"\n".join([chunk.content for chunk in document_chunks])}"
    logger.info(f"prompt: {prompt}")

    response = generate(prompt)
    logger.debug(f"response: {response}")

    return response
