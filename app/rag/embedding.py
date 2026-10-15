from abc import ABC, abstractmethod
from openai import OpenAI

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

class RealEmbeddingModel(EmbeddingModel):
    """
    真实 Embedding Provider。

    当前使用 OpenAI Embedding API。
    """

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
    ):
        self.client = OpenAI()
        self.model_name = model_name


    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        调用真实 Embedding API。

        输入:
            text

        输出:
            embedding vector
        """

        response = self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )

        return response.data[0].embedding

class FakeEmbeddingModel(EmbeddingModel):
    """
    测试使用的假 Embedding。

    后续真实模型替换时，
    不需要修改调用方。
    """

    def embed(self, text: str) -> list[float]:
        return [float(len(text))]
    
class LocalEmbeddingModel(EmbeddingModel):
    """
    本地真实 Embedding。

    使用 Sentence Transformer 模型生成语义向量。
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-zh-v1.5",
    ):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            model_name
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        vector = self.model.encode(
            text
        )

        return vector.tolist()