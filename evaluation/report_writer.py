from pathlib import Path
from datetime import datetime


def write_markdown_report(
    results: list[dict],
    hit_rate: float,
    output_path: str,
):
    """
    将 Evaluation 结果写入 Markdown Report。

    Args:
        results:
            每个 Query 的 Evaluation 结果

        hit_rate:
            当前 Evaluation 的 Hit Rate

        output_path:
            Markdown 文件保存位置
    """

    path = Path(output_path)

    # 确保目录存在
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    lines.append(
        "# Retrieval Evaluation Report\n"
    )

    lines.append(
        f"Generated Time: {datetime.now()}\n"
    )

    lines.append(
        "## Summary\n"
    )

    lines.append(
        f"- Total Queries: {len(results)}\n"
    )

    lines.append(
        f"- Hit Rate: {hit_rate:.2%}\n"
    )

    lines.append(
        "\n---\n"
    )


    lines.append(
        "## Query Results\n"
    )


    for result in results:

        lines.append(
        f"""
        ## {result['query_id']}

        ### Question

        {result['question']}


        ### Expected Source

        {result['expected_source']}


        ### Retrieved Results

        """
        )


        for index, item in enumerate(
            result["retrieved_results"],
            start=1,
        ):

            lines.append(
                f"""
            {index}. Document ID:

            `{item['document_id']}`


            Chunk ID:

            `{item['chunk_id']}`


            Position:

            `{item['metadata'].get('position', 'unknown')}`


            Score:

            `{item['score']}`


            Content:

            > {item['text']}

            """
            )


        status = (
            "✅ HIT"
            if result["hit"]
            else "❌ MISS"
        )


        lines.append(
        f"""
        ### Result

        {status}

        """
        )


        if result["failure_note"]:

            lines.append(
                f"""
            ### Failure Note

            {result['failure_note']}

            """
            )


        lines.append(
            "\n---\n"
        )


    path.write_text(
        "".join(lines),
        encoding="utf-8",
    )