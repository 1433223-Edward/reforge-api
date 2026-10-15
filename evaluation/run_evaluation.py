import json
from pathlib import Path

from app.rag.embedding import LocalEmbeddingModel
from app.rag.vector_index import VectorIndex
from app.rag.retriever import Retriever
from app.rag.ingestion import IngestionPipeline

from evaluation.evaluator import (
    evaluate_retrieval,
    calculate_hit_rate,
)
# 当前项目根目录
BASE_DIR = Path(__file__).parent

DOCUMENT_DIR = BASE_DIR / "documents"
DATASET_PATH = BASE_DIR / "datasets" / "rag_baseline.json"


def load_dataset():
    """
    加载 Evaluation Query Dataset。

    这里只负责读取实验数据，
    不参与 RAG 逻辑。
    """

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def build_rag_pipeline():
    """
    创建一个用于实验的 RAG Pipeline。

    使用 FakeEmbedding,
    因为当前目标是建立 Baseline。
    """

    embedding_model = LocalEmbeddingModel()

    vector_index = VectorIndex()

    ingestion = IngestionPipeline(
        embedding_model=embedding_model,
        vector_index=vector_index,
    )

    # 将 Evaluation Documents 加入索引
    for file_path in DOCUMENT_DIR.glob("*.md"):
        ingestion.ingest(
            str(file_path)
        )

    retriever = Retriever(
        embedding_model=embedding_model,
        vector_index=vector_index,
    )

    return retriever

def main():

    dataset = load_dataset()

    retriever = build_rag_pipeline()

    print(
        "\n===== RAG Baseline Evaluation =====\n"
    )

    evaluation_results = []


    for query in dataset["queries"]:

        retrieved = retriever.retrieve(
            query=query["question"],
            top_k=3,
        )

        result = evaluate_retrieval(
            query,
            retrieved,
        )

        evaluation_results.append(
            result
        )


    hit_rate = calculate_hit_rate(
        evaluation_results
    )


    print(
        f"Hit Rate: {hit_rate:.2%}"
    )

    from evaluation.report_writer import (
        write_markdown_report,
    )

    REPORT_PATH = (
        "evaluation/reports/"
        "retrieval_report.md"
    )

    write_markdown_report(
        results=evaluation_results,
        hit_rate=hit_rate,
        output_path=REPORT_PATH,
    )

if __name__ == "__main__":
    main()