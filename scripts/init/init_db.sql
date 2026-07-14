CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS ingestion_runs
(
    id                UUID PRIMARY KEY,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    chunking_strategy TEXT        NOT NULL,
    embedding_config  JSONB       NOT NULL,
    chunking_config   JSONB       NOT NULL
);

CREATE TABLE IF NOT EXISTS document_chunks
(
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

    source           text        NOT NULL,
    content          text        NOT NULL,
    chunk_index      INTEGER     NOT NULL,

    tags             TEXT[]      NOT NULL DEFAULT '{}'::TEXT[],
    metadata         JSONB       NOT NULL DEFAULT '{}'::JSONB,

    ingestion_run_id UUID        NOT NULL
        REFERENCES ingestion_runs (id)
            ON DELETE CASCADE,

    CONSTRAINT document_chunks_run_source_index_unique
        UNIQUE (ingestion_run_id, source, chunk_index)
);

CREATE INDEX IF NOT EXISTS document_chunks_ingestion_run_idx
    ON document_chunks (ingestion_run_id);

CREATE TABLE IF NOT EXISTS chunk_embeddings_768
(
    document_chunk_id  INTEGER PRIMARY KEY
        REFERENCES document_chunks (id)
            ON DELETE CASCADE,

    embedding vector(768) NOT NULL
);

CREATE INDEX IF NOT EXISTS chunks_embedding_768_embedding_idx
    ON chunk_embeddings_768
        USING hnsw (embedding vector_cosine_ops);