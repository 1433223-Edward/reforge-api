from pathlib import Path

from app.rag.models import Document


def load_text_file(file_path: str) -> Document:
    """
    读取本地文本文件，并转换为 Document 模型。

    Loader 的职责：
    1. 找到文件
    2. 读取内容
    3. 创建 Document
    """

    path = Path(file_path)

    content = path.read_text(
        encoding="utf-8"
    )

    return Document(
        document_id=path.stem,
        title=path.stem,
        content=content,
        metadata={
            "source": str(path)
        }
    )

