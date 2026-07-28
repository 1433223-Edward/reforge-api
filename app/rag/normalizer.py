import re


def normalize_text(text: str) -> str:
    """
    对原始文本进行最小化清理。

    目标：
    1. 删除首尾无意义空白
    2. 减少连续空行
    """

    # 去除文本开头和结尾的空白
    text = text.strip()

    # 将连续多个换行压缩成最多一个换行
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text