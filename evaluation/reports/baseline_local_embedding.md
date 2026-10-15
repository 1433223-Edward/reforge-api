# Baseline Retrieval Report v1


## Configuration

Embedding:
LocalEmbedding
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
Retrieved: ['fastapi.md', 'fastapi.md', 'rag.md']
Result: HIT
----------------------------------------
Query: RAG 系统中 Embedding 和 Vector Index 的作用是什么？
Expected: rag.md
Retrieved: ['rag.md', 'rag.md', 'rag.md']
Result: HIT
----------------------------------------
Query: 为什么测试时需要隔离外部 API？
Expected: testing.md
Retrieved: ['testing.md', 'testing.md', 'testing.md']
Result: HIT
----------------------------------------
Query: RAG 从 Document 到最终回答经历哪些步骤？
Expected: rag.md
Retrieved: ['rag.md', 'rag.md', 'rag.md']
Result: HIT

===== Summary =====
Hit Rate: 5/5
