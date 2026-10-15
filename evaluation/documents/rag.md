# Retrieval Augmented Generation Introduction

RAG（Retrieval Augmented Generation）是一种结合检索和生成的大语言模型应用架构。

RAG 系统首先加载 Document，然后对文本进行 Normalization 和 Chunking。

Chunk 会通过 Embedding Model 转换为向量，并存储到 Vector Index。

用户输入 Query 后，Retriever 会搜索相关 Chunk。

检索结果会作为 Context 提供给 LLM，帮助模型生成更加准确的回答。