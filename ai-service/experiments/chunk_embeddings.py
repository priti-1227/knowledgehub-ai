from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


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
# 2. Split document into chunks
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

chunks = splitter.split_text(text)

print("TOTAL CHUNKS:", len(chunks))


# --------------------------------------------------
# 3. Load BGE embedding model
# --------------------------------------------------

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


# --------------------------------------------------
# 4. Generate embeddings for every chunk
# --------------------------------------------------

embeddings = model.encode(chunks)


# --------------------------------------------------
# 5. Display results
# --------------------------------------------------

for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

    print("\n" + "=" * 70)
    print(f"CHUNK {i + 1}")
    print("=" * 70)

    print(chunk)

    print("\nVECTOR DIMENSION:")
    print(len(embedding))

    print("\nFIRST 5 VECTOR VALUES:")
    print(embedding[:5])