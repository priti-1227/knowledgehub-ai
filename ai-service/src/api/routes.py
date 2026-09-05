from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from src.api.dependencies import (
    get_rag_service,
)
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
)
from src.rag_service import RAGService
from src.security.access_context import (
    AccessContext,
)
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    IngestDocumentRequest,
    IngestDocumentResponse,
)

from src.ingestion.ingest_service import IngestionService
from src.api.dependencies import (
    get_ingestion_service,
    get_rag_service,
)
from src.api.security import (
    verify_service_api_key,
)


router = APIRouter(
    prefix="/api/v1",
    dependencies=[
        Depends(verify_service_api_key),
    ],
)

@router.get("/health")
def health_check():
    """
    Basic liveness endpoint.
    """

    return {
        "status": "ok",
        "service": "knowledgehub-ai",
    }


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,

    rag_service: Annotated[
        RAGService,
        Depends(get_rag_service),
    ],
):

    access_context = AccessContext(
        user_id=request.user_id,
        department=request.department,
        roles=tuple(request.roles),
        is_admin=request.is_admin,
    )

    result = rag_service.answer(
        question=request.question,

        top_k=request.top_k,

        similarity_threshold=(
            request.similarity_threshold
        ),

        access_context=access_context,
    )

    return result
    
@router.post(
    "/documents/ingest",
    response_model=IngestDocumentResponse,
)
def ingest_document(
    request: IngestDocumentRequest,

    ingestion_service: Annotated[
        IngestionService,
        Depends(get_ingestion_service),
    ],
):

    result = ingestion_service.ingest(
        file_path=request.file_path,
        document_name=request.document_name,
        department=request.department,
    )

    return result