from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer("BAAI/bge-small-en-v1.5")


documents = [

    "Employees receive 24 days of annual leave every year.",
    "Employees can work remotely up to two days per week.",
    "Employees must complete security training every six months.",
    "The company provides health insurance to all full-time employees.",
    "Employees must use their company email for official communication.",
]


query = "Can I work from home?"


document_embeddings = model.encode(documents)
query_embedding = model.encode(query)


scores = cos_sim(
    query_embedding,
    document_embeddings,
)[0]


results = []

for document, score in zip(documents, scores):
    results.append(
        {
            "document": document,
            "score": float(score),
        }
    )


results.sort(
    key=lambda item: item["score"],
    reverse=True,
)


print(f"\nQuery: {query}\n")

for index, result in enumerate(results, start=1):
    print(
        f"{index}. "
        f"{result['score']:.4f} "
        f"| {result['document']}"
    )