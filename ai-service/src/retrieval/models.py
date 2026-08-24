from dataclasses import dataclass


@dataclass
class RetrievalResult:
    """
    Represents one retrieved chunk.
    """

    chunk_id: int
    document_id: int
    document_version_id: int
    document_name: str
    chunk_index: int
    content: str
    page_number: int | None
    score: float
    metadata: dict