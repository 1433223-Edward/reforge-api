# Project Reforge LLM Service

A structured and testable FastAPI backend service with configurable LLM providers, asynchronous model calls, dependency injection, and provider error mapping.

## Features

* FastAPI REST API
* Pydantic request and response validation
* Asynchronous `/chat` endpoint
* Configurable Fake and OpenAI LLM providers
* Environment-based configuration
* Dependency Injection for application components
* Provider-neutral application exceptions
* Safe HTTP error mapping
* Automated tests without real network dependencies
* External HTTP service example with error handling
* Mini RAG pipeline with document ingestion and retrieval
* Document chunking and embedding abstraction
* Minimal vector index and similarity search
* Context construction with source tracking

## Project Structure

```text
app/
├── clients/
│   └── llm_client.py
├── config.py
├── exceptions.py
├── external_client.py
├── main.py
├── schemas.py
├── rag/
│   ├── models.py
│   ├── loader.py
│   ├── normalizer.py
│   ├── chunker.py
│   ├── embedding.py
│   ├── vector_index.py
│   ├── retriever.py
│   ├── context_builder.py
│   └── service.py


tests/
├── test_chat.py
├── test_external_check.py
├── test_llm_client.py
└── test_path_debug.py
```

## Requirements

* Python 3.12
* uv

## Installation

Clone the repository and enter the project directory:

```powershell
git clone <repository-url>
cd reforge-api
```

Install the project dependencies:

```powershell
uv sync
```

## Configuration

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Default local configuration:

```dotenv
APP_NAME="Project Reforge LLM Service"
EXTERNAL_API_BASE_URL="https://httpbin.org"

LLM_PROVIDER="fake"
LLM_MODEL="replace-with-model-available-to-your-account"
LLM_API_KEY=""
```

Supported LLM providers:

```text
fake
openai
```

### Fake Provider

The Fake provider does not require network access or an API key:

```dotenv
LLM_PROVIDER="fake"
LLM_API_KEY=""
```

### OpenAI Provider

To use the OpenAI provider:

```dotenv
LLM_PROVIDER="openai"
LLM_MODEL="replace-with-model-available-to-your-account"
LLM_API_KEY="replace-with-your-real-api-key"
```

Never commit `.env` or a real API key to Git.

## Run the Application

```powershell
uv run uvicorn app.main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `POST /chat`

Request:

```json
{
  "message": "hello"
}
```

Fake provider response:

```json
{
  "response": "Fake AI response to: hello"
}
```

Validation behavior:

```text
Missing or invalid fields → 422
Blank message → 400
LLM configuration failure → 500
LLM provider connection failure → 502
LLM provider rate limit → 503
```

### `GET /external-check`

Checks an external HTTP dependency and returns a stable application response.

Example response:

```json
{
  "source": "reforge",
  "upstream_status": 200
}
```

External dependency failures are mapped to HTTP 502.

## Run Tests

```powershell
uv run python -m pytest -v
```

The automated tests use Stub and Fake implementations and do not require a real OpenAI API request.

Tests cover:

* Request and response validation
* Blank input handling
* Dependency overrides
* External HTTP failure mapping
* Fake and OpenAI client construction
* Missing API key behavior
* Provider SDK exception translation
* Application exception to HTTP response mapping
* Internal error information protection

## Architecture

```text
Client Request
↓
Uvicorn
↓
FastAPI
↓
Pydantic Request Validation
↓
Dependency Resolution
↓
LLMClient Abstraction
↓
FakeLLMClient or OpenAILLMClient
↓
Application-level Error Mapping
↓
Pydantic Response Validation
↓
HTTP Response
```

## Error Boundary

```text
Provider SDK Exception
↓
Application-level LLM Exception
↓
HTTPException
↓
Safe Public Response
```

Internal error details are logged on the server and are not returned directly to API clients.

## Current Limitations

* No streaming response
* No conversation memory
* No authentication for `/chat`
* No advanced RAG framework/No Agent framework
* No application-level retry or circuit breaker
* Real OpenAI verification requires a valid API key and model access

## Week 1 Scope

This project was built as the Week 1 Engineering Reset deliverable for Project Reforge.

The Week 1 scope focuses on:

* Python project structure
* Type hints
* Pydantic
* FastAPI
* HTTP and REST
* Async/Await
* Environment variables
* Logging and error handling
* Dependency Injection
* pytest
* Git and project documentation

## Week 2 Scope

This project was extended with a Mini RAG pipeline as the Week 2 RAG Foundation deliverable.

The Week 2 scope focuses on:

* Document ingestion
* Text normalization
* Chunking strategy
* Embedding abstraction
* Vector similarity search
* Retriever design
* Context construction
* Grounded answer generation
* Basic retrieval evaluation