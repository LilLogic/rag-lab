# RAG Lab

A local Retrieval-Augmented Generation system built from scratch with Python, Ollama, PostgreSQL, and pgvector.

The project is designed to make the main RAG engineering concerns explicit and testable:

* document ingestion and chunking;
* metadata extraction;
* embedding generation;
* versioned corpora;
* semantic retrieval;
* retrieval evaluation;
* context-grounded answer generation.

High-level RAG frameworks are intentionally avoided so that data flows, interfaces, SQL queries, failure modes, and architectural decisions remain visible.

## Architecture

```text
Text documents
      |
      v
Metadata extraction
      |
      v
Fixed-size overlapping chunking
      |
      v
Embedding generation
      |
      v
Versioned ingestion run
      |
      v
PostgreSQL + pgvector
      |
      v
Vector retrieval
      |
      +---- optional tag filtering
      |
      v
Retrieved chunks
      |
      v
Local LLM answer generation
```

## Current capabilities

### Versioned ingestion

The ingestion pipeline:

1. reads `.txt` files from `data/raw_docs`;
2. extracts document-level tags;
3. splits documents into overlapping chunks;
4. generates an embedding for each chunk;
5. creates a new ingestion run;
6. stores the chunks and embeddings under that run.

Previous ingestion runs are preserved. This allows several indexed versions of the corpus to coexist in the same database.

Each ingestion run records:

* its UUID;
* its creation timestamp;
* the chunking strategy and configuration;
* the embedding model and vector dimension.

Retrieval, evaluation, and answer generation operate on one explicitly selected ingestion run.

### Semantic retrieval

Questions are embedded using the model configured for the selected ingestion run.

Retrieval supports:

* vector similarity search using pgvector;
* strict isolation by ingestion-run UUID;
* configurable top-K;
* optional tag filtering;
* precomputed query embeddings;
* structured retrieved-chunk results.

### Retrieval evaluation

The evaluation dataset is stored in:

```text
data/evaluation/eval_dataset.json
```

The current metrics are:

* Hit@1;
* Hit@3;
* Hit@K;
* Mean Reciprocal Rank;
* Precision@K;
* Recall@K.

Each evaluation execution creates a timestamped directory under:

```text
reports/evaluation/
```

with:

```text
config.json
summary.json
details.json
```

The report configuration includes the exact ingestion-run UUID used for the evaluation.

### Answer generation

The answer pipeline:

1. embeds the user question;
2. retrieves relevant chunks from the selected ingestion run;
3. builds a prompt containing the original question and retrieved context;
4. generates a response with the configured local LLM.

Generated answers currently return plain text without structured citations.

## Technology stack

* Python 3.12
* PostgreSQL 18
* pgvector
* Docker Compose
* Ollama
* Psycopg 3
* pytest

Default models:

```text
Embedding: nomic-embed-text
Generation: qwen2.5:14b
```

The current embedding storage uses 768-dimensional vectors.

## Database model

The schema is defined in:

```text
scripts/init/init_db.sql
```

Main tables:

```text
ingestion_runs
    id UUID
    created_at
    chunking_strategy
    chunking_config JSONB
    embedding_config JSONB

document_chunks
    id
    created_at
    ingestion_run_id
    source
    content
    chunk_index
    tags
    metadata

chunk_embeddings_768
    document_chunk_id
    embedding vector(768)
```

Each chunk belongs to exactly one ingestion run.

Embeddings are stored separately from chunk content and linked through a foreign key. An HNSW cosine-distance index supports vector retrieval.

## Requirements

Install:

* Python 3.12;
* Docker with Docker Compose;
* Ollama.

Pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:14b
```

Ollama must be running for ingestion, retrieval, evaluation, metadata extraction, and answer generation.

## Setup

Clone the repository:

```bash
git clone https://github.com/LilLogic/rag-lab.git
cd rag-lab
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux or macOS:

```bash
cp .env.example .env
```

Start PostgreSQL:

```bash
docker compose up -d
```

Run commands from the repository root so Python can resolve the `src` package.

## Environment configuration

The main environment variables are:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag_lab
DB_USER=postgres
DB_PASSWORD=postgres

OLLAMA_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=qwen2.5:14b

DEFAULT_INGESTION_RUN_ID=
```

`DEFAULT_INGESTION_RUN_ID` is initially empty because no ingestion run exists yet.

Ingestion does not require this value. Retrieval, evaluation, and answer generation do.

## Ingest documents

Place `.txt` files in:

```text
data/raw_docs/
```

Run:

```bash
python scripts/init/ingest_docs.py
```

The script creates a new ingestion run and outputs its UUID.

Copy that UUID into `.env`:

```dotenv
DEFAULT_INGESTION_RUN_ID=<generated-uuid>
```

This value selects the default corpus used by the retrieval-related scripts.

Running ingestion again creates another ingestion run without deleting previous runs.

## Usage

Run semantic retrieval:

```bash
python scripts/retrieve.py
```

Run retrieval evaluation:

```bash
python scripts/evaluate.py
```

Generate a context-grounded answer:

```bash
python scripts/answer_question.py
```

These scripts use the run selected by `DEFAULT_INGESTION_RUN_ID`.

When the variable is absent, they fail early with an explicit configuration error.

Questions, top-K values, and optional tag filters are currently configured directly in the scripts.

## Testing

Run the complete test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src
```

The suite contains:

* unit tests for isolated application logic;
* integration tests using PostgreSQL and pgvector.

The retrieval integration test creates two temporary ingestion runs and verifies that retrieval cannot return a chunk belonging to another run, even when that chunk is the globally closest vector match.

Integration tests require the PostgreSQL container to be running.

Test database inserts execute inside a transaction and are rolled back after each test.

## Reset the database

Stop the containers and delete the PostgreSQL volume:

```bash
docker compose down -v
```

Recreate the database:

```bash
docker compose up -d
```

Run ingestion again:

```bash
python scripts/init/ingest_docs.py
```

Update `DEFAULT_INGESTION_RUN_ID` with the newly generated UUID.

## Project structure

```text
rag-lab/
├── data/
│   ├── evaluation/
│   └── raw_docs/
├── reports/
│   └── evaluation/
├── scripts/
│   ├── init/
│   │   ├── ingest_docs.py
│   │   └── init_db.sql
│   ├── answer_question.py
│   ├── evaluate.py
│   └── retrieve.py
├── src/
│   ├── client/
│   ├── config/
│   ├── evaluation/
│   ├── ingestion/
│   ├── llm/
│   ├── models/
│   ├── pipeline/
│   ├── retrieval/
│   └── utils/
├── tests/
│   ├── integration/
│   └── unit test directories
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Current limitations

* Only plain-text documents are supported.
* Chunking is fixed-size and character-based.
* Tags are extracted once per document.
* Retrieval uses dense vectors only.
* Hybrid retrieval and reranking are not implemented.
* Generated answers do not include structured source citations.
* Evaluation currently focuses on retrieval rather than answer quality or faithfulness.
* The embedding storage dimension is fixed at 768.
* Ingestion runs are selected manually by UUID.
* There is no API or graphical interface.

## Planned exploration

Potential next steps include:

* alternative chunking strategies;
* comparison of multiple ingestion runs;
* hybrid lexical and vector retrieval;
* reranking;
* metadata-filtering experiments;
* structured source citations;
* answer-faithfulness evaluation;
* support for multiple embedding dimensions;
* human-readable corpus names and run selection;
* observability, CI, API, and deployment.

## License

No open-source license is currently included.

Public visibility does not grant permission to reuse, modify, or redistribute the source code.
