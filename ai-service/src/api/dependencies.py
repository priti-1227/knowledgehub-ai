from functools import lru_cache

from src.embeddings.embedder import Embedder
from src.llm.config import LLMConfig
from src.llm.llm_factory import create_llm_client
from src.prompts.prompt_builder import PromptBuilder
from src.rag_service import RAGService
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.grounding import GroundingValidator
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import PostgresVectorStore
from src.chunking.chunker import DocumentChunker
from src.ingestion.document_repository import DocumentRepository
from src.ingestion.ingest_service import IngestionService
from src.ingestion.pdf_loader import PDFLoader


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    """
    Build the RAG service once and reuse it.
    """

    embedder = Embedder()

    vector_store = PostgresVectorStore()

    retriever = Retriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    config = LLMConfig()

    llm_client = create_llm_client(
        config
    )

    return RAGService(
        retriever=retriever,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        llm_client=llm_client,
        grounding_validator=GroundingValidator(
            minimum_score=0.55
        ),
    )
@lru_cache(maxsize=1)
def get_ingestion_service() -> IngestionService:
    """
    Build and reuse the document ingestion service.
    """

    return IngestionService(
        loader=PDFLoader(),

        chunker=DocumentChunker(
            chunk_size=500,
            chunk_overlap=50,
        ),

        embedder=Embedder(),

        vector_store=PostgresVectorStore(),

        repository=DocumentRepository(),
    )