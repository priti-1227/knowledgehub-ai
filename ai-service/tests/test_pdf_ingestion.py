from pathlib import Path

import fitz

from src.chunking.chunker import DocumentChunker
from src.embeddings.embedder import Embedder
from src.ingestion.ingest_service import IngestionService
from src.ingestion.pdf_loader import PDFLoader
from src.vectordb.vector_store import PostgresVectorStore


def create_test_pdf(path: Path):

    pdf = fitz.open()

    page1 = pdf.new_page()

    page1.insert_text(
        (50, 50),
        """
        Work From Home Policy

        Employees are allowed to work from home
        up to three days per week.

        Employees must obtain approval from their
        reporting manager before working remotely.
        """,
    )

    page2 = pdf.new_page()

    page2.insert_text(
        (50, 50),
        """
        Leave Policy

        Employees receive casual leave,
        sick leave, and earned leave.

        Leave requests must be submitted
        through the employee portal.
        """,
    )

    pdf.save(path)
    pdf.close()


def test_pdf_ingestion(tmp_path):

    pdf_path = (
        tmp_path / "company_policy.pdf"
    )

    create_test_pdf(pdf_path)

    loader = PDFLoader()

    chunker = DocumentChunker(
        chunk_size=300,
        chunk_overlap=30,
    )

    embedder = Embedder()

    vector_store = PostgresVectorStore()

    ingestion_service = IngestionService(
        loader=loader,
        chunker=chunker,
        embedder=embedder,
        vector_store=vector_store,
    )

    chunk_count = ingestion_service.ingest(
        file_path=str(pdf_path),
        document_id=2001,
    )

    assert chunk_count > 0

    print("\nINGESTION COMPLETE")
    print("CHUNKS STORED:", chunk_count)

    query = "How many days can employees work from home?"

    query_embedding = embedder.embed_query(
        query
    )

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
    )

    assert results

    print("\nQUESTION:")
    print(query)

    print("\nSEARCH RESULTS:")

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print("\n" + "=" * 60)
        print(f"RANK: {rank}")
        print(
            f"DOCUMENT: "
            f"{result['document_name']}"
        )
        print(
            f"PAGE: "
            f"{result['page_number']}"
        )
        print(
            f"SCORE: "
            f"{result['score']:.4f}"
        )
        print(
            f"CONTENT:\n"
            f"{result['content']}"
        )

    assert results[0]["page_number"] == 1