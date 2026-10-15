import math
from app.rag.models import Chunk


class VectorIndex:
    """
    最小向量索引。

    保存:
    - chunk 文本
    - 对应 vector

    提供:
    - similarity search
    """

    def __init__(self):
        self.items = []

    def add(
        self,
        chunk: Chunk,
        vector: list[float],
    ):
        """
        保存 chunk 和它的向量。
        """

        self.items.append(
        {
            "chunk_id": chunk.chunk_id,

            "document_id": chunk.document_id,

            "text": chunk.text,

            "metadata": chunk.metadata,

            "vector": vector,
        }
    )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
    ) -> list[dict]:
        """
        根据相似度返回最相关 chunk。
        """

        results = []

        for item in self.items:
            score = cosine_similarity(
                query_vector,
                item["vector"],
            )

            results.append(
                {
                    "chunk_id": item["chunk_id"],

                    "document_id": item["document_id"],

                    "text": item["text"],

                    "metadata": item["metadata"],

                    "score": score,
                }
            )

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return results[:top_k]


def cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:
    """
    计算两个向量的余弦相似度。
    """

    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = math.sqrt(
        sum(x * x for x in a)
    )

    norm_b = math.sqrt(
        sum(y * y for y in b)
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)