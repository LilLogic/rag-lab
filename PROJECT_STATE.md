# Project State

Last Updated: June 2026

## Project Goal

Build a RAG (Retrieval-Augmented Generation) system from scratch to learn RAG engineering concepts and create a portfolio project demonstrating:

* Document ingestion
* Chunking strategies
* Embeddings
* Vector search
* Retrieval evaluation
* LLM-based answer generation

---

## Current Architecture

```text
Documents (.txt)
    ↓
Chunking (fixed size + overlap)
    ↓
nomic-embed-text
    ↓
PostgreSQL + pgvector
    ↓
Vector Retrieval
    ↓
Prompt Assembly
    ↓
qwen2.5:14b
    ↓
Answer
```

---

## Completed

### Repository

* [x] Git repository created
* [x] Public GitHub repository published
* [x] SSH authentication configured
* [x] Add `README.md`
* [x] Add `project_state.md`

### Infrastructure

* [x] Docker Compose setup
* [x] PostgreSQL container
* [x] pgvector extension
* [x] Persistent volume configuration
* [x] Database initialization script

### Ingestion Pipeline

* [x] Document loader
* [x] Fixed-size chunking
* [x] Chunk overlap support
* [x] Embedding generation with `nomic-embed-text`
* [x] Vector storage in PostgreSQL

### Retrieval

* [x] Question embedding
* [x] Similarity search using pgvector
* [x] Top-K retrieval
* [x] Source tracking

### Generation

* [x] Prompt construction
* [x] Context injection
* [x] Answer generation using `qwen2.5:14b`

### Evaluation

* [x] Evaluation dataset support
* [x] Retrieval evaluation script
* [x] Hit@K metrics
* [x] MRR metric
* [x] Precision@K metric
* [x] Recall@K metric

---

## Current Dataset

Technical documents generated for experimentation.

Topics include:

* Retrieval-Augmented Generation (RAG)
* Cache Invalidation
* Chunk Overlap Strategies
* Vector Clocks
* Kubernetes
* Distributed Systems

Current evaluation dataset:

* ~4 manually curated questions

---

## In Progress

### Evaluation Dataset Expansion

Goal:

* Increase from 4 questions to 20-50 questions
* Improve metric reliability
* Cover multiple retrieval scenarios

---

## Next Tasks

### High Priority

* [ ] Expand evaluation dataset
* [ ] Add retrieval failure analysis
* [ ] Review retrieved chunks manually
* [ ] Identify common retrieval mistakes
* [ ] Improve repository code formatting
* [ ] Update GitHub repository description

### Medium Priority

* [ ] Add metadata support to documents
* [ ] Store document metadata in PostgreSQL
* [ ] Support metadata filtering during retrieval
* [ ] Compare different chunk sizes
* [ ] Compare different overlap values
* [ ] Benchmark alternative embedding models

### Low Priority

* [ ] Add BM25 retrieval
* [ ] Implement hybrid search
* [ ] Add reranking step
* [ ] Evaluate retrieval improvements

---

## Future Experiments

Potential areas to explore after the core retrieval pipeline is well evaluated:

* Hybrid Retrieval (BM25 + Dense Retrieval)
* Cross-Encoder Reranking
* Query Expansion
* Multi-Query Retrieval
* Parent-Child Retrieval
* Context Compression
* Larger Real-World Document Collections
* Evaluation Dashboard
* Simple Web UI

---

## Current Status

The core end-to-end RAG pipeline is operational.

Current focus:

1. Strengthen evaluation.
2. Expand the evaluation dataset.
3. Measure retrieval quality.
4. Improve retrieval before adding advanced RAG techniques.

No major architectural blockers identified.
