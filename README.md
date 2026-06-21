# RAG Lab

A Retrieval-Augmented Generation (RAG) system built with PostgreSQL/pgvector and local LLMs through Ollama.

The project demonstrates the core components of a modern RAG pipeline:

* Document ingestion
* Text chunking
* Embedding generation
* Vector storage
* Semantic retrieval
* Retrieval evaluation

This repository is intended as a learning and portfolio project focused on AI Engineering and RAG system design.

---

## Architecture

```text
Documents (.txt)
        ↓
Chunking
        ↓
Embeddings (Ollama)
        ↓
PostgreSQL + pgvector
        ↓
Vector Similarity Search
        ↓
Retrieved Context
        ↓
LLM Response
```

---

## Tech Stack

* Python 3.12+
* PostgreSQL 18
* pgvector
* Docker Compose
* Ollama
* Psycopg 3
* Requests

---

## Project Structure

```text
rag_lab/
│
├── data/
│   ├── docs/
│   └── evaluation/
│       └── eval_dataset.json
│
├── scripts/
│   ├── ingest_docs.py
│   └── init_db.sql
│
├── src/
│   ├── client/
│   │   ├── embedding_client.py
│   │   ├── llm_client.py
│   │   └── postgres_client.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── evaluation/
│   │   └── eval_dataset.py
│   │
│   └── search.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Requirements

* Python 3.12+
* Docker Desktop
* Ollama

Required Ollama models:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:14b
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd rag_lab
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Update values if needed.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_lab
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

OLLAMA_URL=http://localhost:11434

EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=qwen2.5:14b
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

This will:

* Start PostgreSQL with pgvector
* Create the database
* Execute `scripts/init_db.sql`
* Create a persistent Docker volume

### 6. Ingest documents

```bash
python scripts/ingest_docs.py
```

This will:

1. Load documents from `data/docs`
2. Split documents into chunks
3. Generate embeddings
4. Store chunks and embeddings in PostgreSQL

---

## Configuration

Application configuration is managed through environment variables loaded from `.env`.

Configuration is centralized in:

```text
src/config/settings.py
```

---

## Evaluation

The repository contains an evaluation dataset located in:

```text
data/evaluation/eval_dataset.json
```

The evaluation framework is used to assess retrieval quality and source attribution accuracy.

Current evaluation focuses on validating whether the retrieval layer returns the expected source documents for a given query.

---

## Database

The PostgreSQL schema is defined in:

```text
scripts/init_db.sql
```

The schema is automatically initialized during the first container startup.

To completely reset the database:

```bash
docker compose down -v
docker compose up -d
```

Then rerun ingestion:

```bash
python scripts/ingest_docs.py
```

---

## Future Improvements

* Hybrid search (vector + keyword search)
* Reranking
* Retrieval metrics (Recall@K, MRR)
* Automated evaluation reports
* API interface
* Web UI
* Support for multiple embedding models
* Metadata filtering
* Production-ready deployment

---

## Learning Objectives

This project was built to explore:

* Retrieval-Augmented Generation (RAG)
* Vector databases
* Embedding models
* Semantic search
* PostgreSQL + pgvector
* Local LLM deployment with Ollama
* Retrieval evaluation methodologies

---

## License

This project is provided for educational and portfolio purposes.
