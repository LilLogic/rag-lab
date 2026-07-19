# RAG Lab

A local Retrieval-Augmented Generation system built from scratch with Python, Ollama, PostgreSQL, and pgvector.

The project implements the main stages of a RAG pipeline:

* text document ingestion;
* fixed-size overlapping chunking;
* LLM-based metadata extraction;
* local embedding generation;
* vector storage in PostgreSQL;
* semantic retrieval with optional metadata filtering;
* retrieval evaluation;
* context-grounded answer generation with a local LLM.

The repository is an engineering lab and portfolio project for exploring RAG architecture, retrieval quality, evaluation methodologies, and production-oriented Python structure without hiding the implementation behind a high-level RAG framework.

## Architecture

```text
Text documents
      |
      v
LLM metadata extraction
      |
      v
Fixed-size overlapping chunking
      |
      v
Embedding generation with Ollama
      |
      v
PostgreSQL + pgvector
      |
      v
Vector similarity search
      |
      +---- optional tag filtering
      |
      v
Retrieved document chunks
      |
      v
Prompt construction
      |
      v
Local LLM response
```

## Current capabilities

### Document ingestion

The ingestion pipeline:

1. reads `.txt` files from `data/raw_docs`;
2. extracts document-level tags with the configured LLM;
3. splits each document into overlapping chunks;
4. generates an embedding for every chunk;
5. stores the chunks and their metadata in PostgreSQL.

The stored metadata includes:

* source filename;
* extracted tags;
* chunk index;
* embedding model;
* chunk size;
* chunk overlap;
* creation timestamp.

Running ingestion truncates the existing `document_chunks` table before rebuilding the corpus.

### Semantic retrieval

Questions are embedded through Ollama and compared with stored vectors using pgvector cosine distance.

Retrieval supports:

* configurable top-K retrieval;
* optional filtering by document tags;
* reusable database cursors for batch evaluation;
* structured `RetrievedChunk` results.

When tags are supplied, PostgreSQL array-overlap filtering is applied before vector ranking.

### Answer generation

The answer pipeline:

1. retrieves the five most relevant chunks;
2. combines their content into a prompt;
3. instructs the LLM to answer using only the provided sources;
4. returns the generated response.

The current implementation returns the answer as plain text. It does not yet expose source citations in the generated response.

### Retrieval evaluation

The evaluation framework reads questions and expected source documents from:

```text
data/evaluation/eval_dataset.json
```

It calculates:

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

Each run contains:

```text
config.json
summary.json
details.json
```

This records the retrieval configuration, aggregate metrics, retrieved sources, chunk contents, and per-question results.

## Technology stack

* Python 3.12
* PostgreSQL 18
* pgvector
* Docker Compose
* Ollama
* Psycopg 3
* Requests
* python-dotenv
* pytest
* pytest-cov

Default local models:

```text
Embedding model: nomic-embed-text
Generation model: qwen2.5:14b
```

The current database schema expects 768-dimensional embedding vectors.

## Project structure

```text
rag-lab/
├── data/
│   ├── evaluation/
│   │   └── eval_dataset.json
│   └── raw_docs/
│       └── *.txt
├── reports/
│   └── evaluation/
├── scripts/
│   ├── init/
│   │   ├── ingest_docs.py
│   │   └── init_db.sql
│   ├── answer_question.py
│   ├── ask_llm.py
│   ├── evaluate.py
│   └── retrieve.py
├── src/
│   ├── chunking/
│   │   └── chunker.py
│   ├── client/
│   │   ├── embedding_client.py
│   │   ├── llm_client.py
│   │   └── postgres_client.py
│   ├── config/
│   │   ├── logging_config.py
│   │   ├── paths.py
│   │   └── settings.py
│   ├── evaluation/
│   │   ├── evaluator.py
│   │   ├── metrics.py
│   │   └── report_writer.py
│   ├── ingestion/
│   │   └── ingester.py
│   ├── llm/
│   │   └── tag_extractor.py
│   ├── models/
│   │   ├── document_chunk.py
│   │   └── retrieved_chunk.py
│   ├── pipeline/
│   │   └── pipeline.py
│   └── retrieval/
│       └── retriever.py
├── tests/
│   ├── chunking/
│   ├── evaluation/
│   ├── llm/
│   └── models/
├── .env.example
├── .python_version
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requirements

Install the following tools:

* Python 3.12;
* Docker with Docker Compose;
* Ollama.

Pull the required Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:14b
```

Ollama must be running when performing ingestion, retrieval, metadata extraction, evaluation, or answer generation.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/LilLogic/rag-lab.git
cd rag-lab
```

Run commands from the repository root so Python can resolve the `src` package.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` from the supplied example.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux or macOS:

```bash
cp .env.example .env
```

Default configuration:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_lab
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

OLLAMA_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=qwen2.5:14b

CHUNK_SIZE=400
CHUNK_OVERLAP=80
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

Check the container status:

```bash
docker compose ps
```

Docker Compose starts PostgreSQL with pgvector, initializes the schema from `scripts/init/init_db.sql`, configures a health check, and creates a persistent volume.

### 6. Ingest documents

Place `.txt` files under:

```text
data/raw_docs/
```

Run ingestion:

```bash
python scripts/init/ingest_docs.py
```

Ingestion extracts tags with the configured LLM and generates an embedding for each chunk, so Ollama must be available.

## Usage

### Generate an answer

```bash
python scripts/answer_question.py
```

The example question is currently defined directly in the script:

```python
question = "What is RAG?"
```

The application pipeline can also be called from Python:

```python
from src.pipeline.pipeline import answer_question

response = answer_question("What is RAG?")
print(response)
```

### Run semantic retrieval

```bash
python scripts/retrieve.py
```

The example script performs retrieval with both a question and tag filters:

```python
results = retrieve(
    question="Explain cache invalidation.",
    top_k=5,
    tags=["caching", "expiration"],
)
```

Retrieval without metadata filtering:

```python
from src.retrieval.retriever import retrieve

results = retrieve(
    question="Explain cache invalidation.",
    top_k=5,
)

for chunk in results:
    print(chunk.source)
    print(chunk.distance)
    print(chunk.content)
```

Retrieval with metadata filtering:

```python
results = retrieve(
    question="Explain cache invalidation.",
    top_k=5,
    tags=["caching", "expiration"],
)
```

A chunk is eligible when at least one of its stored tags overlaps with the supplied tag list.

### Test the LLM client

```bash
python scripts/scratch_llm.py
```

This is a development utility for experimenting directly with the configured generation model.

### Run retrieval evaluation

```bash
python scripts/evaluate.py
```

The evaluator:

1. loads the evaluation dataset;
2. retrieves the top-K chunks for each question;
3. compares retrieved sources with expected sources;
4. calculates aggregate retrieval metrics;
5. prints per-question and aggregate results;
6. writes a timestamped evaluation report.

An evaluation case follows this structure:

```json
{
  "question": "What is cache invalidation?",
  "expected_sources": [
    "cache_invalidation.txt"
  ]
}
```

## Evaluation metrics

### Hit@K

Returns whether at least one expected source appears in the first K retrieved results.

### Mean Reciprocal Rank

Measures how highly the first relevant source is ranked. Earlier relevant results receive a higher score.

### Precision@K

Measures the proportion of the first K retrieved results whose source belongs to the expected source set.

### Recall@K

Measures the proportion of expected sources found within the first K retrieved results.

The current framework evaluates retrieval at the source-document level. It does not yet evaluate answer correctness, answer relevance, faithfulness, or citation accuracy.

## Running tests

Run the complete test suite:

```bash
pytest
```

Run the suite with coverage:

```bash
pytest --cov=src
```

The tests are organized by component under the root-level `tests` directory.

## Database

The PostgreSQL schema is defined in:

```text
scripts/init/init_db.sql
```

The `document_chunks` table contains:

* an identity primary key;
* source filename;
* chunk content;
* a 768-dimensional vector embedding;
* document tags;
* chunk index;
* embedding model;
* chunk size;
* chunk overlap;
* creation timestamp.

An HNSW index using cosine-distance vector operations is created on the embedding column.

### Reset the database

Stop PostgreSQL and delete its persistent volume:

```bash
docker compose down -v
```

Recreate the database:

```bash
docker compose up -d
```

Rebuild the corpus:

```bash
python scripts/init/ingest_docs.py
```

Deleting the volume permanently removes the locally stored database contents.

## Configuration

Environment settings are loaded from `.env` and centralized in:

```text
src/config/settings.py
```

Repository-relative paths are centralized in:

```text
src/config/paths.py
```

Executable scripts initialize application logging through:

```text
src/config/logging_config.py
```

Library modules use named loggers without configuring global logging themselves.

## Current limitations

* Only plain-text documents are ingested.
* Chunking uses character counts rather than tokens or semantic boundaries.
* Tags are extracted once per document and applied to all of its chunks.
* Retrieval uses dense vector similarity only.
* Query tags must currently be supplied explicitly.
* There is no keyword-search or hybrid-search stage.
* There is no reranking stage.
* Retrieved chunks are concatenated directly into the generation prompt.
* Generated answers do not currently include structured source citations.
* Evaluation is limited to source-level retrieval quality.
* The embedding dimension is fixed at 768 in the database schema.
* The project has no API or graphical interface.

## Potential next steps

* hybrid vector and keyword retrieval;
* candidate reranking;
* automatic query-tag extraction;
* retrieval filtering experiments;
* alternative chunking strategies;
* configurable prompt templates;
* source citations in generated answers;
* answer relevance and faithfulness evaluation;
* support for additional embedding models;
* integration testing for database-backed components;
* continuous integration;
* API and interactive interfaces;
* deployment and observability.

## Project objectives

RAG Lab is designed to make each stage of a RAG system explicit and independently testable:

* document preparation;
* metadata extraction;
* chunking;
* embedding generation;
* vector persistence;
* retrieval;
* retrieval evaluation;
* prompt construction;
* answer generation.

The project favors direct implementation over framework abstraction so that architectural choices and their impact on retrieval quality remain visible.

## License

No open-source license is currently included in the repository.

Public visibility alone does not grant permission to reuse, modify, or redistribute the source code.
