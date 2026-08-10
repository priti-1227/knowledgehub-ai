import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Embedding model
# -----------------------------

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


# -----------------------------
# 2. Persistent Chroma database
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# -----------------------------
# 3. Create / get collection
# -----------------------------

collection = client.get_or_create_collection(
    name="knowledgehub_documents"
)


# -----------------------------
# 4. Documents
# -----------------------------

documents = [
    "Employees can work remotely up to two days per week.",
    "Employees receive 24 days of annual leave every year.",
    "Employees must complete security training every six months.",
    "The company provides health insurance to all full-time employees.",
]


# -----------------------------
# 5. Generate embeddings
# -----------------------------

embeddings = model.encode(
    documents
).tolist()


# -----------------------------
# 6. Store documents
# -----------------------------

collection.upsert(
    ids=[
        "chunk_1",
        "chunk_2",
        "chunk_3",
        "chunk_4",
    ],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {
            "document_id": "doc_001",
            "department": "HR",
        },
        {
            "document_id": "doc_001",
            "department": "HR",
        },
        {
            "document_id": "doc_002",
            "department": "IT",
        },
        {
            "document_id": "doc_003",
            "department": "HR",
        },
    ],
)


print("Documents stored successfully.")


# -----------------------------
# 7. Search
# -----------------------------

query = "Can I work from home?"

query_embedding = model.encode(
    [query]
).tolist()


results = collection.query(
    query_embeddings=query_embedding,
    n_results=2,
)


# -----------------------------
# 8. Display results
# -----------------------------

print("\nQuery:")
print(query)

print("\nResults:")

for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    print("\nDocument:")
    print(document)

    print("Metadata:")
    print(metadata)

    print("Distance:")
    print(distance)