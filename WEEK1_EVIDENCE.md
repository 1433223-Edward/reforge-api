# Week 1 Evidence — Engineering Reset

## Mission

Build a structured, testable Python backend service capable of supporting an asynchronous LLM API call.

## Final Application

The project provides:

```text
POST /chat
GET /external-check
```

The `/chat` endpoint supports:

```text
Pydantic request validation
Business validation
LLM Client abstraction
Fake and OpenAI providers
Environment-based configuration
Async/Await
Provider-neutral exception mapping
Stable HTTP responses
```

## Verification Command

```powershell
uv run python -m pytest -v
```

## Automated Test Result

```text
Final result: <replace-with-real-result>
Total tests: <replace-with-real-count>
Failed tests: 0
```

Do not estimate these values. Copy them from the final verified test run.

## API Evidence

### Chat Success

```text
POST /chat
Expected status: 200
```

Example Fake response:

```json
{
  "response": "Fake AI response to: hello"
}
```

### Missing Message

```text
Expected status: 422
```

### Blank Message

```text
Expected status: 400
```

### LLM Configuration Failure

```text
Expected status: 500
```

### LLM Connection Failure

```text
Expected status: 502
```

### LLM Rate Limit

```text
Expected status: 503
```

### External Dependency Failure

```text
Expected status: 502
```

## Architecture Evidence

```text
.env
↓
Settings
↓
get_settings
↓
get_llm_client
↓
LLMClient
├── FakeLLMClient
└── OpenAILLMClient
↓
async /chat
↓
ChatResponse
```

## Error Boundary Evidence

```text
OpenAI SDK Exception
↓
Application-level LLM Exception
↓
HTTPException
↓
Safe HTTP Response
```

The automated tests verify both transitions independently:

```text
SDK Exception → Application Exception
Application Exception → HTTP Response
```

## Test Isolation Evidence

Automated tests do not require:

```text
A real API key
A real OpenAI request
A stable external network
Deterministic model output
```

The tests use:

```text
StubLLMClient
FailingOpenAISDK
ErrorLLMClient
dependency_overrides
monkeypatch
```

## Secret Safety Evidence

```text
.env is ignored by Git
.env.example contains placeholders only
No real API key is committed
```

Verification commands:

```powershell
git check-ignore -v .env
git ls-files .env
```

Expected:

```text
.env is ignored
git ls-files .env returns no output
```

## Git Evidence

```text
Final commit: <replace-with-real-commit-hash>
Working tree: <clean or describe remaining files>
```

Verification commands:

```powershell
git log -1 --oneline
git status --short
```

## Manual Verification

```text
Fake provider: <PASS or Pending>
OpenAI provider: <PASS or Pending — no valid API key>
External check: <PASS or Pending>
```

Do not mark real OpenAI verification as PASS unless an actual provider request completed successfully.

## Known Limitations

```text
No streaming
No conversation memory
No authentication
No RAG
No Agent framework
No circuit breaker
No custom retry policy
```

## Week 1 Completion Statement

```text
Code implementation: <PASS or Pending>
Automated tests: <PASS or Pending>
README: <PASS or Pending>
Git evidence: <PASS or Pending>
Real OpenAI integration verification: <PASS or Pending>
```
