from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request sent by the main backend to the AI service.
    """

    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    user_id: int

    department: str | None = None

    roles: list[str] = []

    is_admin: bool = False

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    similarity_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )


class SourceResponse(BaseModel):

    chunk_id: int

    document_id: int

    document_version_id: int

    document_name: str

    page_number: int | None

    score: float


class ChatResponse(BaseModel):

    answer: str

    grounded: bool

    grounding_reason: str

    best_score: float | None

    model: str | None

    provider: str | None

    sources: list[SourceResponse]
class IngestDocumentRequest(BaseModel):
    """
    Request sent by the main backend when a document
    needs to be processed by the AI service.
    """

    file_path: str = Field(
        min_length=1,
        max_length=2000,
    )

    document_name: str = Field(
        min_length=1,
        max_length=500,
    )

    department: str | None = Field(
        default=None,
        max_length=200,
    )


class IngestDocumentResponse(BaseModel):
    """
    Result of the AI indexing process.
    """

    status: str

    document_id: int | None = None

    version_id: int | None = None

    version_number: int | None = None

    chunks: int = 0
