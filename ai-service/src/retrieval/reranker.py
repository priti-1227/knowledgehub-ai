from sentence_transformers import CrossEncoder

from src.retrieval.models import RetrievalResult


class Reranker:
    """
    Second-stage retrieval model.

    Vector search finds candidate chunks.
    The reranker then evaluates the question
    together with each candidate and reorders
    them by relevance.
    """

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        ),
    ):
        self.model_name = model_name

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        question: str,
        results: list[RetrievalResult],
        top_k: int = 3,
    ) -> list[RetrievalResult]:

        if not results:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        pairs = [
            (
                question,
                result.content,
            )
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        scored_results = list(
            zip(
                results,
                scores,
            )
        )

        scored_results.sort(
            key=lambda item: float(item[1]),
            reverse=True,
        )

        reranked_results = []

        for result, score in scored_results[:top_k]:

            # Preserve original vector score
            # inside metadata for debugging.
            metadata = dict(
                result.metadata or {}
            )

            metadata[
                "vector_score"
            ] = result.score

            metadata[
                "reranker_score"
            ] = float(score)

            reranked_results.append(
                RetrievalResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    document_version_id=(
                        result.document_version_id
                    ),
                    document_name=(
                        result.document_name
                    ),
                    chunk_index=result.chunk_index,
                    content=result.content,
                    page_number=result.page_number,

                    # Temporarily use reranker
                    # score as the final score.
                    score=float(score),

                    metadata=metadata,
                )
            )

        return reranked_results