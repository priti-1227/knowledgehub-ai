from src.chunking.chunker import DocumentChunker


def test_document_chunking():

    text = """
    Work From Home Policy

    Employees are allowed to work from home up to three days per week.
    Employees must obtain approval from their reporting manager before
    working remotely.

    Employees working from home must remain available during normal
    working hours.
    """

    chunker = DocumentChunker(
        chunk_size=200,
        chunk_overlap=30,
    )

    chunks = chunker.split_text(text)

    assert len(chunks) > 1
    assert all(len(chunk) > 0 for chunk in chunks)

    print("\nChunks created:", len(chunks))

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i + 1} ---")
        print(chunk)