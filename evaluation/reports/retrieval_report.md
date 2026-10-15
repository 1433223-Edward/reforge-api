# Retrieval Evaluation Report
Generated Time: 2026-07-29 10:55:12.548048
## Summary
- Total Queries: 6
- Hit Rate: 83.33%

---
## Query Results

## q001

### Question

FastAPI 如何创建 HTTP Endpoint？


### Expected Source

fastapi.md


### Retrieved Results


1. Source:
`fastapi.md`

Score:
`0.707`

Chunk:

> 响应数据验证。
FastAPI 可以自动生成 OpenAPI 文档，方便开发者测试接口。


2. Source:
`fastapi.md`

Score:
`0.6953`

Chunk:

> # FastAPI Backend Development Guide
FastAPI 是一个基于 Python 的现代 Web 框架，用于快速构建 API 服


3. Source:
`fastapi.md`

Score:
`0.6902`

Chunk:

>  Web 框架，用于快速构建 API 服务。
开发者可以通过定义路径操作函数创建 HTTP Endpoint。
GET 方法通常用于获取数据。
POST 方法通


### Result

✅ HIT


---

## q002

### Question

FastAPI 如何验证请求参数？


### Expected Source

fastapi.md


### Retrieved Results


1. Source:
`fastapi.md`

Score:
`0.7438`

Chunk:

> 响应数据验证。
FastAPI 可以自动生成 OpenAPI 文档，方便开发者测试接口。


2. Source:
`fastapi.md`

Score:
`0.7227`

Chunk:

> 方法通常用于获取数据。
POST 方法通常用于提交数据。
FastAPI 使用 Pydantic 模型进行请求参数验证和响应数据验证。
FastAPI 可以自动


3. Source:
`rag.md`

Score:
`0.6021`

Chunk:

> nk。
检索结果会作为 Context 提供给 LLM，帮助模型生成更加准确的回答。


### Result

✅ HIT


---

## q003

### Question

RAG 系统中 Embedding 和 Vector Index 的作用是什么？


### Expected Source

rag.md


### Retrieved Results


1. Source:
`rag.md`

Score:
`0.6176`

Chunk:

> nt，然后对文本进行 Normalization 和 Chunking。
Chunk 会通过 Embedding Model 转换为向量，并存储到 Vector


2. Source:
`rag.md`

Score:
`0.5846`

Chunk:

> el 转换为向量，并存储到 Vector Index。
用户输入 Query 后，Retriever 会搜索相关 Chunk。
检索结果会作为 Context 


3. Source:
`rag.md`

Score:
`0.5535`

Chunk:

> Augmented Generation）是一种结合检索和生成的大语言模型应用架构。
RAG 系统首先加载 Document，然后对文本进行 Normaliza


### Result

✅ HIT


---

## q004

### Question

为什么测试时需要隔离外部 API？


### Expected Source

testing.md


### Retrieved Results


1. Source:
`testing.md`

Score:
`0.6666`

Chunk:

> # Python Testing Engineering
软件测试用于验证系统行为是否符合预期。
单元测试通常需要隔离外部依赖，例如数据库、第三方 API 或网


2. Source:
`testing.md`

Score:
`0.5158`

Chunk:

> 部依赖，例如数据库、第三方 API 或网络服务。
Mock 和 Fake Object 可以替代真实依赖，使测试更加稳定。
pytest 是 Python 中常


3. Source:
`testing.md`

Score:
`0.5148`

Chunk:

> 。
pytest 是 Python 中常用的自动化测试框架。
良好的测试应该关注输入、输出以及异常行为。


### Result

✅ HIT


---

## q005

### Question

RAG 从 Document 到最终回答经历哪些步骤？


### Expected Source

rag.md


### Retrieved Results


1. Source:
`rag.md`

Score:
`0.5997`

Chunk:

> nk。
检索结果会作为 Context 提供给 LLM，帮助模型生成更加准确的回答。


2. Source:
`rag.md`

Score:
`0.5744`

Chunk:

> Augmented Generation）是一种结合检索和生成的大语言模型应用架构。
RAG 系统首先加载 Document，然后对文本进行 Normaliza


3. Source:
`rag.md`

Score:
`0.5553`

Chunk:

> el 转换为向量，并存储到 Vector Index。
用户输入 Query 后，Retriever 会搜索相关 Chunk。
检索结果会作为 Context 


### Result

✅ HIT


---

## q006

### Question

Kubernetes 如何管理大规模容器集群？


### Expected Source

kubernetes.md


### Retrieved Results


1. Source:
`rag.md`

Score:
`0.4533`

Chunk:

> Augmented Generation）是一种结合检索和生成的大语言模型应用架构。
RAG 系统首先加载 Document，然后对文本进行 Normaliza


2. Source:
`fastapi.md`

Score:
`0.4221`

Chunk:

> 响应数据验证。
FastAPI 可以自动生成 OpenAPI 文档，方便开发者测试接口。


3. Source:
`rag.md`

Score:
`0.4012`

Chunk:

> el 转换为向量，并存储到 Vector Index。
用户输入 Query 后，Retriever 会搜索相关 Chunk。
检索结果会作为 Context 


### Result

❌ MISS


### Failure Note

Expected source was not found in top-k retrieval.


---
