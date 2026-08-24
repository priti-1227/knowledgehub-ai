from pathlib import Path

from src.chunking.chunker import DocumentChunker
from src.embeddings.embedder import Embedder
from src.ingestion.document_repository import (
    DocumentRepository,
)
from src.ingestion.file_hash import (
    calculate_file_hash,
)
from src.ingestion.pdf_loader import PDFLoader
from src.vectordb.vector_store import (
    PostgresVectorStore,
)


class IngestionService:
    """
    Production-style document ingestion workflow.

    PDF
      ↓
    Hash
      ↓
    Duplicate detection
      ↓
    Document/version creation
      ↓
    PDF extraction
      ↓
    Chunking
      ↓
    Embeddings
      ↓
    PostgreSQL + pgvector
      ↓
    ACTIVE
    """

    def __init__(
        self,
        loader: PDFLoader,
        chunker: DocumentChunker,
        embedder: Embedder,
        vector_store: PostgresVectorStore,
        repository: DocumentRepository,
    ):

        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.repository = repository

    def ingest(
        self,
        file_path: str,
        document_name: str,
        department: str | None = None,
    ) -> dict:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # ------------------------------------------------
        # STEP 1: Calculate file hash
        # ------------------------------------------------

        file_hash = calculate_file_hash(
            file_path
        )

        print(
            f"FILE HASH: {file_hash}"
        )

        # ------------------------------------------------
        # STEP 2: Duplicate detection
        # ------------------------------------------------

        existing_version_id = (
            self.repository.find_version_by_hash(
                file_hash
            )
        )

        if existing_version_id:

            print(
                "DUPLICATE FILE DETECTED."
            )

            return {
                "status": "duplicate",
                "version_id": existing_version_id,
                "chunks": 0,
            }

        # ------------------------------------------------
        # STEP 3: Find/create logical document
        # ------------------------------------------------

        document_id = (
            self.repository.find_document_by_name(
                document_name
            )
        )

        if document_id is None:

            document_id = (
                self.repository.create_document(
                    name=document_name,
                    department=department,
                )
            )

            print(
                f"CREATED DOCUMENT: {document_id}"
            )

        else:

            print(
                f"USING EXISTING DOCUMENT: "
                f"{document_id}"
            )

        # ------------------------------------------------
        # STEP 4: Create new version
        # ------------------------------------------------

        version_number = (
            self.repository.get_next_version_number(
                document_id
            )
        )

        version_id = (
            self.repository.create_version(
                document_id=document_id,
                version_number=version_number,
                file_name=path.name,
                file_path=str(path),
                file_hash=file_hash,
                status="processing",
            )
        )

        print(
            f"CREATED VERSION: "
            f"{version_number}"
        )

        try:

            # --------------------------------------------
            # STEP 5: Extract PDF
            # --------------------------------------------

            pages = self.loader.load(
                file_path
            )

            if not pages:
                raise ValueError(
                    "PDF contains no extractable text."
                )

            # --------------------------------------------
            # STEP 6: Chunk
            # --------------------------------------------

            chunks = []

            global_chunk_index = 0

            for page in pages:

                page_chunks = (
                    self.chunker.split_document(
                        page
                    )
                )

                for chunk in page_chunks:

                    chunks.append(
                        {
                            "document_id": document_id,
                            "document_version_id": version_id,
                            "document_name": document_name,
                            "chunk_index": global_chunk_index,
                            "content": chunk["content"],
                            "page_number": page.metadata[
                                "page_number"
                            ],
                            "metadata": {
                                "filename": path.name,
                                "page_number": page.metadata[
                                    "page_number"
                                ],
                                "version": version_number,
                            },
                        }
                    )

                    global_chunk_index += 1

            if not chunks:
                raise ValueError(
                    "No chunks were generated."
                )

            print(
                f"GENERATED CHUNKS: "
                f"{len(chunks)}"
            )

            # --------------------------------------------
            # STEP 7: Embeddings
            # --------------------------------------------

            texts = [
                chunk["content"]
                for chunk in chunks
            ]

            embeddings = (
                self.embedder.embed_documents(
                    texts
                )
            )

            print(
                f"GENERATED EMBEDDINGS: "
                f"{len(embeddings)}"
            )

            # --------------------------------------------
            # STEP 8: Store vectors
            # --------------------------------------------

            self.vector_store.add(
                documents=chunks,
                embeddings=embeddings,
            )

            # --------------------------------------------
            # STEP 9: Mark version ACTIVE
            # --------------------------------------------

            self.repository.update_version_status(
                version_id,
                "active",
            )

            print(
                "INGESTION COMPLETED."
            )

            return {
                "status": "success",
                "document_id": document_id,
                "version_id": version_id,
                "version_number": version_number,
                "chunks": len(chunks),
            }

        except Exception:

            self.repository.update_version_status(
                version_id,
                "failed",
            )

            raise