from app.rag.embedding import LocalEmbeddingModel
from app.rag.vector_index import VectorIndex
from app.rag.retriever import Retriever
from app.rag.ingestion import IngestionPipeline

from evaluation.run_evaluation import (
    load_dataset,
)

from evaluation.evaluator import (
    evaluate_retrieval,
    calculate_hit_rate,
)


from pathlib import Path


BASE_DIR = Path(__file__).parent

DOCUMENT_DIR = (
    BASE_DIR / "documents"
)


def build_rag_pipeline(
    chunk_size: int,
    overlap: int,
):
    """
    根据不同 Chunk 配置，
    创建独立 RAG Pipeline。

    每次实验都会创建新的 VectorIndex,
    避免不同实验数据污染。
    """

    embedding_model = (
        LocalEmbeddingModel()
    )

    vector_index = VectorIndex()


    ingestion = IngestionPipeline(
        embedding_model=embedding_model,
        vector_index=vector_index,
        chunk_size=chunk_size,
        overlap=overlap,
    )


    for file_path in DOCUMENT_DIR.glob(
        "*.md"
    ):
        ingestion.ingest(
            str(file_path)
        )


    retriever = Retriever(
        embedding_model=embedding_model,
        vector_index=vector_index,
    )


    return retriever



def run_experiment(
    experiment_name: str,
    chunk_size: int,
    overlap: int,
):
    """
    执行一次 Chunking Experiment。
    """

    print("\n" + "=" * 50)

    print(
        f"Experiment: {experiment_name}"
    )

    print(
        f"Chunk Size: {chunk_size}"
    )

    print(
        f"Overlap: {overlap}"
    )


    retriever = build_rag_pipeline(
        chunk_size=chunk_size,
        overlap=overlap,
    )


    dataset = load_dataset()


    results = []


    for query in dataset["queries"]:

        retrieved_results = (
            retriever.retrieve(
                query=query["question"],
                top_k=3,
            )
        )


        result = evaluate_retrieval(
            query,
            retrieved_results,
        )


        results.append(
            result
        )


    hit_rate = calculate_hit_rate(
        results
    )


    print(
        f"Hit Rate: {hit_rate:.2%}"
    )


    return {
        "experiment": experiment_name,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "hit_rate": hit_rate,
    }



def main():

    experiments = [

        {
            "name": "chunk_80_overlap_20",
            "chunk_size": 80,
            "overlap": 20,
        },

        {
            "name": "chunk_150_overlap_30",
            "chunk_size": 150,
            "overlap": 30,
        },

    ]


    experiment_results = []


    for experiment in experiments:

        result = run_experiment(
            experiment_name=experiment["name"],
            chunk_size=experiment["chunk_size"],
            overlap=experiment["overlap"],
        )

        experiment_results.append(
            result
        )

    print(
        "\n\n===== Experiment Summary ====="
    )


    for result in experiment_results:

        print(
            f"""
        {result['experiment']}

        Chunk Size:
        {result['chunk_size']}

        Overlap:
        {result['overlap']}

        Hit Rate:
        {result['hit_rate']:.2%}

        """
                )


if __name__ == "__main__":
    main()