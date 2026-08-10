from langchain_text_splitters import RecursiveCharacterTextSplitter


text = """
KnowledgeHub AI is an enterprise knowledge management system.

Employees can access company documents through the KnowledgeHub system.

Employees can work remotely up to two days per week with manager approval.

Employees receive 24 days of annual leave every year.

Employees must complete security training every six months.

The company provides health insurance to all full-time employees.
"""


splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
)


chunks = splitter.split_text(text)


for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk)