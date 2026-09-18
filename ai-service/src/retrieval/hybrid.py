from src.retrieval.models import RetrievalResult


class HybridFusion:

    def fuse(
        self,
        vector_results: list[RetrievalResult],
        keyword_results: list[dict],
        top_k: int = 10,
        rrf_k: int = 60,
    ) -> list[RetrievalResult]:

        scores = {}

        results_map = {}

        # Vector ranking
        for rank, result in enumerate(
            vector_results,
            start=1,
        ):
            chunk_id = result.chunk_id

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (rrf_k + rank)
            )

            results_map[chunk_id] = result

        # Keyword ranking
        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):
            chunk_id = result["id"]

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (rrf_k + rank)
            )

            if chunk_id not in results_map:

                results_map[chunk_id] = (
                    RetrievalResult(
                        chunk_id=result["id"],
                        document_id=(
                            result["document_id"]
                        ),
                        document_version_id=(
                            result[
                                "document_version_id"
                            ]
                        ),
                        document_name=(
                            result["document_name"]
                        ),
                        chunk_index=(
                            result["chunk_index"]
                        ),
                        content=result["content"],
                        page_number=(
                            result["page_number"]
                        ),
                        score=0.0,
                        metadata=(
                            result["metadata"]
                        ),
                    )
                )

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        output = []

        for chunk_id in ranked_ids[:top_k]:

            result = results_map[
                chunk_id
            ]

            metadata = dict(
                result.metadata or {}
            )

            metadata["rrf_score"] = (
                scores[chunk_id]
            )

            result.metadata = metadata

            output.append(result)

        return output