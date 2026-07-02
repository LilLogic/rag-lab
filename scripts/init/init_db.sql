CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source text NOT NULL,
    content text NOT NULL,
    embedding vector(768) NOT NULL,

    tags TEXT[] NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding_model TEXT NOT NULL,

    chunk_size INTEGER NOT NULL,
    chunk_overlap INTEGER NOT NULL,

    created_at timestamp without time zone DEFAULT now()
);

CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops);

