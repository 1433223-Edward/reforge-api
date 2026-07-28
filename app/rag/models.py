from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    原始文档模型。

    一个 Document 可以被切分成多个 Chunk。
    """

    document_id: str = Field(
        description="Unique identifier of the document"
    )

    title: str = Field(
        description="Document title"
    )

    content: str = Field(
        description="Original document content"
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Additional document information"
    )


class Chunk(BaseModel):
    """
    文档切分后的检索单位。

    Retriever 后续检索的是 Chunk,而不是完整 Document。
    """

    chunk_id: str = Field(
        description="Unique identifier of the chunk"
    )

    document_id: str = Field(
        description="The source document this chunk belongs to"
    )

    text: str = Field(
        description="Chunk text content"
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Chunk level metadata"
    )