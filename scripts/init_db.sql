CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source text NOT NULL,
    content text NOT NULL,
    embedding vector(768),
    created_at timestamp without time zone DEFAULT now()
);

CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops);

