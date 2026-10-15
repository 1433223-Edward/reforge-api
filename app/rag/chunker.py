from app.rag.models import Chunk 
def chunk_text(
    text: str,
    document_id: str,
    chunk_size: int,
    overlap: int,
) -> list[Chunk]:
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
    chunk_index = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text_content = text[start:end]


        chunks.append(
            Chunk(
                chunk_id=f"{document_id}_{chunk_index}",

                document_id=document_id,

                text=chunk_text_content,

                metadata={
                    "position": str(chunk_index),
                },
            )
        )


        chunk_index += 1

        start += chunk_size - overlap

    return chunks