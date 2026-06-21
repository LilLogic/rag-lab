from src.client.embedding_client import embed_text
from src.client.llm_client import generate
from src.client.postgres_client import get_connection

question = "What is the advantage of small chunks in retrieval?"

print(f"QUESTION:\n")
print(f"{question}")

query_embedding = embed_text(question)[0]

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, source, content, embedding <=> %s::vector AS distance
            FROM document_chunks
            ORDER BY embedding <=> %s::vector
                LIMIT 5;
            """,
            (query_embedding, query_embedding)
        )
        results = cur.fetchall()

context = "\n\n".join([
    f"SOURCE: {row[1]}\nCONTENT:\n{row[2]}"
    for row in results])

print("\nRETRIEVED CHUNKS:\n")

for row in results:
    print("=" * 80)
    print(f"SOURCE: {row[1]}")
    print(f"DISTANCE: {row[3]}")
    print(row[2][:500])

prompt = f"""
You are a RAG assistant.

Answer the question using ONLY the provided context.

For every important statement, mention the corresponding SOURCE.

If the context does not contain enough information, say:
"I don't know based on the provided context."

Context:
{context}

Question:
{question}
"""

answer = generate(prompt)

print("\nANSWER:\n")
print(answer)
