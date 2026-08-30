from src.embeddings.embedder import Embedder
from src.retrieval.retriever import Retriever
from src.security.access_context import AccessContext
from src.vectordb.vector_store import PostgresVectorStore


def test_hr_user_can_access_hr_document():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    user = AccessContext(
        user_id=101,
        department="HR",
        roles=("employee",),
    )

    results = retriever.retrieve(
        question="Can employees work remotely?",
        top_k=3,
        similarity_threshold=0.5,
        access_context=user,
    )

    print("\nHR USER RESULTS")

    for result in results:

        print(
            result.document_name,
            "|",
            result.score,
        )

    assert results

    assert any(
        result.document_name
        == "Work From Home Policy"
        for result in results
    )


def test_engineering_user_cannot_access_hr_document():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    user = AccessContext(
        user_id=202,
        department="Engineering",
        roles=("employee",),
    )

    results = retriever.retrieve(
        question="Can employees work remotely?",
        top_k=3,
        similarity_threshold=0.5,
        access_context=user,
    )

    print("\nENGINEERING USER RESULTS")

    for result in results:

        print(
            result.document_name,
            "|",
            result.score,
        )

    assert all(
        result.document_name
        != "Work From Home Policy"
        for result in results
    )