def build_context(
    results: list[dict],
) -> str:
    """
    将检索结果转换为 LLM Context。

    保留：
    - chunk 内容
    - similarity score
    """

    context_parts = []

    for item in results:
        context_parts.append(
            f"[Score: {item['score']}]\n"
            f"{item['chunk']}"
        )

    return "\n\n".join(context_parts)