from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import InMemoryVectorStore
from src.retrieval.retriever import Retriever


def test_retrieval():

    documents = [
        {
            "content": (
                "Employees are allowed to work from home "
                "up to three days per week."
            ),
            "document_name": "Work From Home Policy",
            "chunk_index": 0,
        },
        {
            "content": (
                "Employees must submit leave requests "
                "through the employee portal."
            ),
            "document_name": "Leave Policy",
            "chunk_index": 1,
        },
        {
            "content": (
                "Employees must maintain regular communication "
                "with their team while working remotely."
            ),
            "document_name": "Work From Home Policy",
            "chunk_index": 2,
        },
    ]

    embedder = Embedder()

    embeddings = embedder.embed_documents(
        [document["content"] for document in documents]
    )

    vector_store = InMemoryVectorStore()

    vector_store.add(
        documents=documents,
        embeddings=embeddings,
    )

    retriever = Retriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query="Can employees work remotely?",
        top_k=2,
    )

    assert len(results) == 2

    assert results[0]["document_name"] == "Work From Home Policy"

    assert results[0]["score"] >= results[1]["score"]

    print("\nQUERY:")
    print("Can employees work remotely?")

    print("\nRESULTS:")

    for result in results:
        print("\n------------------------------")
        print("Document:", result["document_name"])
        print("Chunk:", result["chunk_index"])
        print("Score:", result["score"])
        print("Content:", result["content"])