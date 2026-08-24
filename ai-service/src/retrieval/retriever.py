from src.embeddings.embedder import Embedder
from src.vectordb.vector_store import PostgresVectorStore

from src.retrieval.models import RetrievalResult


class Retriever:
    """
    Converts a user question into an embedding
    and retrieves relevant chunks.
    """

    def __init__(
        self,
        embedder: Embedder,
        vector_store: PostgresVectorStore,
    ):

        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
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

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )

        return [
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