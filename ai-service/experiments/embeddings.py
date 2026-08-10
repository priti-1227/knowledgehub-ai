from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


sentences = [
    "Can employees work remotely?",
    "What is the work from home policy?",
    "What is the company's leave policy?",
]


embeddings = model.encode(sentences)


print("\nVector dimensions:")
for sentence, embedding in zip(sentences, embeddings):
    print(f"{len(embedding)} - {sentence}")


print("\nSimilarity scores:\n")

similarities = cos_sim(embeddings, embeddings)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):

        print(
            f"{similarities[i][j]:.4f}"
            f"  |  "
            f"{sentences[i]}"
            f"  ↔  "
            f"{sentences[j]}"
        )