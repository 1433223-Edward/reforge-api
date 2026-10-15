# Baseline Retrieval Report v1


## Configuration

Embedding:
FakeEmbedding
Index:
Minimal Vector Index

Chunk Size:
80

Overlap:
20

Top K:
3


## Results

===== RAG Baseline Evaluation =====

----------------------------------------
Query: FastAPI 如何创建 HTTP Endpoint？
Expected: fastapi.md
Retrieved: ['fastapi.md', 'fastapi.md', 'fastapi.md']
Result: HIT
----------------------------------------
Query: FastAPI 如何验证请求参数？
Expected: fastapi.md
Retrieved: ['fastapi.md', 'fastapi.md', 'fastapi.md']
Result: HIT
----------------------------------------
Query: RAG 系统中 Embedding 和 Vector Index 的作用是什么？        
Expected: rag.md
Retrieved: ['fastapi.md', 'fastapi.md', 'fastapi.md']
Result: MISS
----------------------------------------
Query: 为什么测试时需要隔离外部 API？
Expected: testing.md
Retrieved: ['fastapi.md', 'fastapi.md', 'fastapi.md']
Result: MISS
----------------------------------------
Query: RAG 从 Document 到最终回答经历哪些步骤？
Expected: rag.md
Retrieved: ['fastapi.md', 'fastapi.md', 'fastapi.md']
Result: MISS

===== Summary =====
Hit Rate: 2/5

## Failure Analysis

Baseline Result:

Hit Rate:
2/5


Main Failure Pattern:

FakeEmbeddingModel only encodes text length.
The vector representation lacks semantic information,
causing unrelated documents with similar length to be retrieved.


Example:

Query:
"RAG 系统中 Embedding 和 Vector Index 的作用是什么？"

Expected:
rag.md

Retrieved:
fastapi.md


Root Cause:
Embedding representation failure.

Not caused by:
- Retriever logic
- VectorIndex search