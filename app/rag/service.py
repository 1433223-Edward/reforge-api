from app.rag.context_builder import build_context
from app.rag.retriever import Retriever


class RAGService:
    """
    RAG 核心业务流程。

    负责连接：
    Retriever
    Context Builder
    LLM
    """

    def __init__(
        self,
        retriever: Retriever,
        llm_client,
    ):
        self.retriever = retriever
        self.llm_client = llm_client

    def query(
        self,
        question: str,
    ) -> dict:
        """
        执行一次 RAG 查询。
        """

        # 1. 检索相关 Chunk
        results = self.retriever.retrieve(
            question
        )

        # 2. 构建给 LLM 的 Context
        context = build_context(
            results
        )

        # 3. 调用 LLM 生成回答
        answer = self.llm_client.generate(
            question,
            context,
        )

        return {
            "answer": answer,
            "sources": results,
        }