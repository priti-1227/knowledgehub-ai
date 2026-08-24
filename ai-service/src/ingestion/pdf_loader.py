from pathlib import Path

import pymupdf

from src.ingestion.document import Document


class PDFLoader:
    """
    Loads a PDF page by page.

    Each page becomes a Document object so that
    page-level metadata is preserved.
    """

    def load(self, file_path: str) -> list[Document]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file, got: {path.suffix}"
            )

        documents = []

        with pymupdf.open(path) as pdf:

            for page_number, page in enumerate(
                pdf,
                start=1,
            ):

                text = page.get_text("text").strip()

                # Skip completely empty pages
                if not text:
                    continue

                documents.append(
                    Document(
                        content=text,
                        source=str(path),
                        metadata={
                            "filename": path.name,
                            "extension": ".pdf",
                            "page_number": page_number,
                            "total_pages": len(pdf),
                        },
                    )
                )

        return documents