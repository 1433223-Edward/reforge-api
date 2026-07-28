from app.rag.embedding import FakeEmbeddingModel
from app.rag.vector_index import VectorIndex
from app.rag.retriever import Retriever


def test_retrieval_returns_related_chunk():
    # 创建 Index
    index = VectorIndex()

    # 添加模拟知识
    index.add(
        chunk="Python was created by Guido van Rossum.",
        vector=[1.0],
    )

    index.add(
        chunk="RAG combines retrieval and generation.",
        vector=[0.1],
    )

    # 创建 Retriever
    retriever = Retriever(
        embedding_model=FakeEmbeddingModel(),
        vector_index=index,
    )

    results = retriever.retrieve(
        "Who created Python?",
        top_k=1,
    )

    assert len(results) == 1

    assert (
        "Python"
        in results[0]["chunk"]
    )