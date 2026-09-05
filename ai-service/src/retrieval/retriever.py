from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import PostgresVectorStore
from src.retrieval.filters import RetrievalFilter
from src.security.access_context import AccessContext

from src.retrieval.models import RetrievalResult
from src.retrieval.reranker import Reranker


class Retriever:
    """
    Converts a user question into an embedding
    and retrieves relevant chunks.
    """

    def __init__(
        self,
        embedder: Embedder,
        vector_store: PostgresVectorStore,
        reranker: Reranker | None = None,
    ):

        self.embedder = embedder
        self.vector_store = vector_store
        self.reranker = reranker

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        access_context=None,
        candidate_k: int | None = None,
) -> list[RetrievalResult]:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        query_embedding = (
            self.embedder.embed_query(
                question
            )
        )

        retrieval_filter = None

        if access_context is not None:

            if access_context.is_admin:

                retrieval_filter = RetrievalFilter(
                    department=None,
                    include_public=True,
                )

            else:

                retrieval_filter = RetrievalFilter(
                    department=(
                        access_context.department
                    ),
                    include_public=True,
                )

        # If reranking is enabled, retrieve more
        # candidates than the final top_k.
        search_k = (
            candidate_k
            if candidate_k is not None
            else (
                max(top_k * 3, 10)
                if self.reranker
                else top_k
            )
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=search_k,
            similarity_threshold=(
                similarity_threshold
            ),
            retrieval_filter=retrieval_filter,
        )

        retrieval_results = [
            RetrievalResult(
                chunk_id=result["id"],
                document_id=result["document_id"],
                document_version_id=result[
                    "document_version_id"
                ],
                document_name=result[
                    "document_name"
                ],
                chunk_index=result["chunk_index"],
                content=result["content"],
                page_number=result["page_number"],
                score=result["score"],
                metadata=result["metadata"],
            )
            for result in results
        ]

        if self.reranker:

            return self.reranker.rerank(
                question=question,
                results=retrieval_results,
                top_k=top_k,
            )

        return retrieval_results[:top_k]