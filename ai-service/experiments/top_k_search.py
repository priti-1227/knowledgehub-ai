from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Sample ERP document
# --------------------------------------------------

text = """
Work From Home Policy

Employees are allowed to work from home up to three days per week.
Employees must obtain approval from their reporting manager before
working remotely.

Employees working from home must remain available during normal
working hours. They must attend all required meetings and maintain
regular communication with their team.

The company may require employees to work from the office when
business requirements demand it.

Leave Policy

Employees receive casual leave, sick leave, and earned leave according
to the company's leave policy. Leave requests must be submitted through
the employee portal and approved by the reporting manager.
"""


# --------------------------------------------------
# 2. Split document
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

chunks = splitter.split_text(text)


# --------------------------------------------------
# 3. Load BGE
# --------------------------------------------------

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


# --------------------------------------------------
# 4. Create embeddings for chunks
# --------------------------------------------------

chunk_embeddings = model.encode(chunks)


# --------------------------------------------------
# 5. User question
# --------------------------------------------------

question = "Can employees work remotely?"


# --------------------------------------------------
# 6. Create question embedding
# --------------------------------------------------

question_embedding = model.encode([question])


# --------------------------------------------------
# 7. Calculate similarity
# --------------------------------------------------

similarities = cosine_similarity(
    question_embedding,
    chunk_embeddings
)[0]


# --------------------------------------------------
# 8. Get Top-K results
# --------------------------------------------------

top_k = 2

top_indices = similarities.argsort()[::-1][:top_k]


# --------------------------------------------------
# 9. Display Top-K chunks
# --------------------------------------------------

print("\nQUESTION:")
print(question)

print("\n" + "=" * 70)
print(f"TOP {top_k} RESULTS")
print("=" * 70)

for rank, index in enumerate(top_indices, start=1):

    print(f"\nRANK: {rank}")
    print(f"CHUNK: {index + 1}")
    print(f"SIMILARITY SCORE: {similarities[index]:.4f}")

    print("\nCONTENT:")
    print(chunks[index])