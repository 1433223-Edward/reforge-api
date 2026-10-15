from app.rag.embedding import (
    FakeEmbeddingModel,
    LocalEmbeddingModel,
)


def test_embedding_adapter():

    text = "RAG combines retrieval and generation."


    fake_model = FakeEmbeddingModel()

    fake_vector = fake_model.embed(
        text
    )

    print("Fake Embedding:")
    print(
        type(fake_vector),
        len(fake_vector),
    )


    local_model = LocalEmbeddingModel()

    local_vector = local_model.embed(
        text
    )

    print("\nlocal Embedding:")
    print(
        type(local_vector),
        len(local_vector),
    )


if __name__ == "__main__":
    test_embedding_adapter()