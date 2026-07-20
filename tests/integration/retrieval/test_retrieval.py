import uuid

from src.ingestion.ingester import insert_document_chunk, insert_ingestion_run, insert_chunk_embedding
from src.models.document_chunk import DocumentChunk
from src.models.ingestion_run import IngestionRun
from src.retrieval.retriever import retrieve_with_cursor
from tests.integration.conftest import db_cursor


def test_retrieval_isolated_by_ingestion_run(db_cursor):
    ingestion_run_a = IngestionRun(
        id=uuid.uuid4(),
        chunking_strategy="fixed_size",
        embedding_config={},
        chunking_config={}
    )

    ingestion_run_b = IngestionRun(
        id=uuid.uuid4(),
        chunking_strategy="fixed_size",
        embedding_config={},
        chunking_config={}
    )

    insert_ingestion_run(cursor=db_cursor, ingestion_run=ingestion_run_a)
    insert_ingestion_run(cursor=db_cursor, ingestion_run=ingestion_run_b)

    document_chunk_a = DocumentChunk(
        source="test_a.txt",
        content="test A",
        chunk_index=0,
        tags=[],
        metadata={},
        ingestion_run_id=ingestion_run_a.id
    )

    document_chunk_b = DocumentChunk(
        source="test_b.txt",
        content="test B",
        chunk_index=0,
        tags=[],
        metadata={},
        ingestion_run_id=ingestion_run_b.id
    )

    document_chunk_id_a = insert_document_chunk(cursor=db_cursor, chunk=document_chunk_a)
    document_chunk_id_b = insert_document_chunk(cursor=db_cursor, chunk=document_chunk_b)

    query_embedding = [1.0] + [0.0] * 767

    run_a_embedding = [0.5] + [1.0] * 767
    run_b_embedding = query_embedding.copy()

    insert_chunk_embedding(cursor=db_cursor, document_chunk_id=document_chunk_id_a, embedding=run_a_embedding)
    insert_chunk_embedding(cursor=db_cursor, document_chunk_id=document_chunk_id_b, embedding=run_b_embedding)

    retrieved_chunks = retrieve_with_cursor(
        cursor=db_cursor,
        ingestion_run=ingestion_run_a,
        embedded_question=query_embedding,
        top_k=5
    )

    assert len(retrieved_chunks) == 1
    assert retrieved_chunks[0].content == document_chunk_a.content
    assert retrieved_chunks[0].source == document_chunk_a.source
