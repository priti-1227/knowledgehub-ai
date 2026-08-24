from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingestion.document import Document


class DocumentChunker:
    """
    Splits documents into smaller chunks while
    preserving source metadata.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_document(
        self,
        document: Document,
    ) -> list[dict]:

        chunks = self.splitter.split_text(
            document.content
        )

        return [
            {
                "content": chunk,
                "chunk_index": index,
                "source": document.source,
                "metadata": document.metadata,
            }
            for index, chunk in enumerate(chunks)
        ]