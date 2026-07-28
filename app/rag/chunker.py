def chunk_text(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """
    将文本切分成多个 chunk。

    参数：
    - chunk_size: 每个 chunk 最大长度
    - overlap: 相邻 chunk 重叠字符数量

    返回：
    - chunk 文本列表
    """

    if chunk_size <= overlap:
        raise ValueError(
            "chunk_size must be greater than overlap"
        )

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        # 下一段向前移动：
        # chunk_size - overlap
        start += chunk_size - overlap

    return chunks