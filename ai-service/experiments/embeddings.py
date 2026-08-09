from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


sentences = [
    "What is the work from home policy?",
    "Can employees work remotely?",
    "What is the company's leave policy?",
]


embeddings = model.encode(sentences)


for sentence, embedding in zip(sentences, embeddings):
    print("\nTEXT:")
    print(sentence)

    print("\nVECTOR DIMENSION:")
    print(len(embedding))

    print("\nFIRST 5 VALUES:")
    print(embedding[:5])