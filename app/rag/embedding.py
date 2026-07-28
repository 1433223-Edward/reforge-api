from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """
    Embedding 抽象接口。

    定义：
    输入文本
    输出向量
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        将文本转换为向量。
        """
        pass


class FakeEmbeddingModel(EmbeddingModel):
    """
    测试使用的假 Embedding。

    后续真实模型替换时，
    不需要修改调用方。
    """

    def embed(self, text: str) -> list[float]:
        return [float(len(text))]