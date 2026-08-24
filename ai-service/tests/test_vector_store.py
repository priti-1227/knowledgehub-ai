from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import PostgresVectorStore


def test_vector_store():

    documents = [
        {
            "document_id": 1001,
            "document_name": "Work From Home Policy",
            "chunk_index": 0,
            "content": (
                "Employees are allowed to work from home "
                "up to three days per week."
            ),
        },
        {
            "document_id": 1001,
            "document_name": "Work From Home Policy",
            "chunk_index": 1,
            "content": (
                "Employees working from home must remain "
                "available during normal working hours."
            ),
        },
        {
            "document_id": 1002,
            "document_name": "Leave Policy",
            "chunk_index": 0,
            "content": (
                "Employees receive casual leave, sick leave "
                "and earned leave."
            ),
        },
    ]

    embedder = Embedder()

    embeddings = embedder.embed_documents(
        [
            document["content"]
            for document in documents
        ]
    )

    vector_store = PostgresVectorStore()

    vector_store.add(
        documents=documents,
        embeddings=embeddings,
    )

    query = "Can employees work remotely?"

    query_embedding = embedder.embed_query(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    assert len(results) == 2

    assert results[0]["document_name"] == "Work From Home Policy"

    assert results[0]["score"] >= results[1]["score"]

    print("\nQUESTION:")
    print(query)

    print("\nTOP RESULTS:")

    for rank, result in enumerate(results, start=1):
        print("\n" + "=" * 60)
        print(f"RANK: {rank}")
        print(f"DOCUMENT: {result['document_name']}")
        print(f"CHUNK: {result['chunk_index']}")
        print(f"SCORE: {result['score']:.4f}")
        print(f"CONTENT:\n{result['content']}")