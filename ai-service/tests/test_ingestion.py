from pathlib import Path

from src.ingestion.loader import TextLoader
from src.chunking.chunker import DocumentChunker


def test_ingestion_pipeline(tmp_path):

    file_path = tmp_path / "work_from_home.txt"

    file_path.write_text(
        """
        Work From Home Policy

        Employees are allowed to work from home
        up to three days per week.

        Employees must obtain approval from their
        reporting manager before working remotely.

        Employees working from home must remain
        available during normal working hours.
        """,
        encoding="utf-8",
    )

    loader = TextLoader()

    document = loader.load(
        str(file_path)
    )

    assert document.content
    assert document.metadata["filename"] == "work_from_home.txt"

    chunker = DocumentChunker(
        chunk_size=150,
        chunk_overlap=30,
    )

    chunks = chunker.split_document(
        document
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk["content"]
        assert "chunk_index" in chunk
        assert chunk["metadata"]["filename"] == "work_from_home.txt"

    print("\nDOCUMENT:")
    print(document)

    print("\nCHUNKS:")

    for chunk in chunks:
        print("\n--------------------")
        print("INDEX:", chunk["chunk_index"])
        print("CONTENT:")
        print(chunk["content"])
        print("METADATA:")
        print(chunk["metadata"])