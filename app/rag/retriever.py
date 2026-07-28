from app.rag.embedding import EmbeddingModel
from app.rag.vector_index import VectorIndex


class Retriever:
    """
    RAG 检索层。

    负责：
    Query → Vector → Search → Results
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_index: VectorIndex,
    ):
        self.embedding_model = embedding_model
        self.vector_index = vector_index

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        根据用户 Query 返回相关 Chunk。
        """

        query_vector = self.embedding_model.embed(
            query
        )

        results = self.vector_index.search(
            query_vector=query_vector,
            top_k=top_k,
        )

        return results