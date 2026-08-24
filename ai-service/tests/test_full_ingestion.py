import pymupdf

from src.chunking.chunker import DocumentChunker
from src.embeddings.embedder import Embedder
from src.ingestion.document_repository import (
    DocumentRepository,
)
from src.ingestion.ingest_service import (
    IngestionService,
)
from src.ingestion.pdf_loader import PDFLoader
from src.vectordb.vector_store import (
    PostgresVectorStore,
)


def create_pdf(path):

    pdf = pymupdf.open()

    page = pdf.new_page()

    page.insert_text(
        (50, 50),
        """
        Work From Home Policy

        Employees are allowed to work from home
        up to three days per week.

        Employees must obtain approval from their
        reporting manager before working remotely.
        """,
    )

    pdf.save(path)
    pdf.close()


def test_full_ingestion(tmp_path):

    pdf_path = (
        tmp_path / "work_from_home.pdf"
    )

    create_pdf(pdf_path)

    service = IngestionService(
        loader=PDFLoader(),

        chunker=DocumentChunker(
            chunk_size=300,
            chunk_overlap=30,
        ),

        embedder=Embedder(),

        vector_store=PostgresVectorStore(),

        repository=DocumentRepository(),
    )

    result = service.ingest(
        file_path=str(pdf_path),
        document_name="Work From Home Policy",
        department="HR",
    )

    print("\nRESULT:")
    print(result)

    assert result["status"] == "success"
    assert result["chunks"] > 0
    assert result["version_number"] == 1