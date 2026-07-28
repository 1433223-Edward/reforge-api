# Project Reforge Week 2 Evidence

## Overview

Week 2 extends the backend foundation into a Mini RAG Service.

The implementation focuses on understanding and building a complete RAG pipeline:

Document
→ Parse
→ Normalize
→ Chunk
→ Embed
→ Index
→ Retrieve
→ Build Context
→ Generate Answer


## Completed Components

### Document Processing

Implemented:

- Document loading
- Text normalization
- Metadata preservation
- Chunk generation


Evidence:

- `app/rag/loader.py`
- `app/rag/normalizer.py`
- `app/rag/chunker.py`
- `app/rag/models.py`


---

### Embedding Layer

Implemented:

- Embedding abstraction
- Fake embedding provider for controlled testing

Evidence:

- `app/rag/embedding.py`


---

### Vector Retrieval

Implemented:

- Minimal vector index
- Similarity search
- Top-k retrieval

Evidence:

- `app/rag/vector_index.py`
- `app/rag/retriever.py`


---

### Context Construction

Implemented:

- Retrieved chunk formatting
- Source information preservation

Evidence:

- `app/rag/context_builder.py`


---

### RAG Service

Implemented:

- Query orchestration
- Retriever integration
- Context building
- LLM provider integration boundary

Evidence:

- `app/rag/service.py`


---

## Verification

Verified behaviors:

- Document can be loaded
- Text can be normalized
- Document can be split into chunks
- Text can be converted into vectors through embedding abstraction
- Vector index can perform similarity search
- Retriever returns top-k chunks
- Context builder creates LLM-ready context
- RAG service returns answer with sources


## Retrieval Evaluation

Basic evaluation:

Scenario:

Query:

"Who created Python?"


Expected:

Retriever returns related chunk containing:

"Python was created by Guido van Rossum."


Evaluation target:

Check retrieval result rather than final generated answer.

Reason:

Retrieval quality and generation quality are separate concerns.


## Architecture Summary

```text
User Query
    ↓
RAG Service
    ↓
Retriever
    ↓
Embedding
    ↓
Vector Index
    ↓
Top-k Chunks
    ↓
Context Builder
    ↓
LLM Provider
    ↓
Answer + Sources