from app.rag.loader import load_text_file
from app.rag.normalizer import normalize_text
from app.rag.chunker import chunk_text
from app.rag.embedding import EmbeddingModel
from app.rag.vector_index import VectorIndex


class IngestionPipeline:
    """
    文档知识入库流程。

    负责：
    Document
    → Chunk
    → Vector
    → Index

    不负责：
    - Query
    - Retrieval
    - Answer Generation
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_index: VectorIndex,
        chunk_size=80,
        overlap=20,
    ):
        self.embedding_model = embedding_model
        self.vector_index = vector_index
        self.chunk_size = chunk_size
        self.overlap = overlap

    def ingest(
        self,
        file_path: str,
    ):
        """
        将一个文档处理并写入 Index。
        """

        # 1. 读取原始文档
        document = load_text_file(
            file_path
        )

        # 2. 清理文本
        normalized_text = normalize_text(
            document.content
        )

        # 3. 切分 Chunk
        chunks = chunk_text(
            normalized_text,
            document_id=document.document_id,
            chunk_size=self.chunk_size,
            overlap=self.overlap,
        )

        # 4. 生成向量并写入索引
        for chunk in chunks:

            vector = self.embedding_model.embed(
                chunk.text
            )

            self.vector_index.add(
                chunk=chunk,
                vector=vector,
            )