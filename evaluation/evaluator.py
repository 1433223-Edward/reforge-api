def evaluate_retrieval(
    query_item: dict,
    retrieved_results: list[dict],
) -> dict:
    """
    评估单个 Query 的检索结果。
    """

    expected_source = (
        query_item["expected_source"]
    )


    retrieved_sources = [
        item["document_id"]
        for item in retrieved_results
    ]


    hit = (
        expected_source
        in retrieved_sources
    )


    return {
        "query_id": query_item["query_id"],

        "question": query_item["question"],

        "expected_source": expected_source,

        "retrieved_results": retrieved_results,

        "retrieved_sources": retrieved_sources,

        "hit": hit,

        "failure_note": (
            None
            if hit
            else
            "Expected document was not retrieved."
        ),
    }


def calculate_hit_rate(
    results: list[dict],
) -> float:
    """
    计算整体命中率。

    Hit Rate =
    命中的 Query 数 / 总 Query 数
    """

    if not results:
        return 0.0

    hits = sum(
        1
        for item in results
        if item["hit"]
    )

    return hits / len(results)