from src.embeddings.embedder import Embedder
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import PostgresVectorStore


def test_retriever():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    question = (
        "Can employees work remotely?"
    )

    results = retriever.retrieve(
        question=question,
        top_k=3,
        similarity_threshold=0.5,
    )

    print("\nQUESTION:")
    print(question)

    print("\nRETRIEVAL RESULTS:")

    for rank, result in enumerate(
        results,
        start=1,
    ):

        print("\n" + "=" * 60)

        print(
            f"RANK: {rank}"
        )

        print(
            f"DOCUMENT: "
            f"{result.document_name}"
        )

        print(
            f"VERSION ID: "
            f"{result.document_version_id}"
        )

        print(
            f"PAGE: "
            f"{result.page_number}"
        )

        print(
            f"SCORE: "
            f"{result.score:.4f}"
        )

        print(
            f"CONTENT:\n"
            f"{result.content}"
        )

    assert results

    assert results[0].score >= 0.5