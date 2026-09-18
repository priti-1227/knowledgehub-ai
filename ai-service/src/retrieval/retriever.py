from src.embeddings.embedder import Embedder

from src.retrieval.filters import RetrievalFilter
from src.retrieval.hybrid import HybridFusion
from src.retrieval.models import RetrievalResult
from src.retrieval.reranker import Reranker

from src.security.access_context import AccessContext


class Retriever:
    """
    Retrieves relevant document chunks.

    Retrieval pipeline:

        Question
            ↓
        Embedding
            ↓
        ┌───────────────┬────────────────┐
        │ Vector Search │ Keyword Search │
        └───────────────┴────────────────┘
                    ↓
             Hybrid Fusion (RRF)
                    ↓
               CrossEncoder
                    ↓
                Top-K results
    """

    def __init__(
        self,
        embedder: Embedder,
        vector_store,
        reranker: Reranker | None = None,
        hybrid_fusion: HybridFusion | None = None,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.reranker = reranker

        self.hybrid_fusion = (
            hybrid_fusion
            if hybrid_fusion is not None
            else HybridFusion()
        )

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        access_context: AccessContext | None = None,
        candidate_k: int | None = None,
    ) -> list[RetrievalResult]:

        # -------------------------------------------------
        # 1. Validate question
        # -------------------------------------------------

        if not question.strip():
            return []

        # -------------------------------------------------
        # 2. Decide candidate search size
        # -------------------------------------------------
        #
        # We retrieve more candidates initially because:
        #
        # vector search
        #        +
        # keyword search
        #        ↓
        # hybrid fusion
        #        ↓
        # reranker
        #
        # needs a broader candidate pool.
        # -------------------------------------------------

        search_k = (
            candidate_k
            if candidate_k is not None
            else max(top_k * 3, 10)
        )

        # -------------------------------------------------
        # 3. Build permission-aware retrieval filter
        # -------------------------------------------------

        retrieval_filter = self._build_filter(
            access_context
        )

        # -------------------------------------------------
        # 4. Create semantic query embedding
        # -------------------------------------------------

        query_embedding = self.embedder.embed_query(
            question
        )

        # -------------------------------------------------
        # 5. Vector search
        # -------------------------------------------------

        vector_rows = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=search_k,
            similarity_threshold=similarity_threshold,
            retrieval_filter=retrieval_filter,
        )

        # -------------------------------------------------
        # 6. Convert vector rows to RetrievalResult
        # -------------------------------------------------

        vector_results = (
            self._convert_vector_results(
                vector_rows
            )
        )

        # -------------------------------------------------
        # 7. Keyword / full-text search
        # -------------------------------------------------

        keyword_rows = (
            self.vector_store.keyword_search(
                query=question,
                top_k=search_k,
                retrieval_filter=retrieval_filter,
            )
        )

        # -------------------------------------------------
        # 8. Hybrid fusion
        # -------------------------------------------------
        #
        # RRF merges rankings from:
        #
        # - semantic vector search
        # - exact keyword search
        #
        # without directly adding incompatible raw scores.
        # -------------------------------------------------

        hybrid_results = (
            self.hybrid_fusion.fuse(
                vector_results=vector_results,
                keyword_results=keyword_rows,
                top_k=search_k,
            )
        )

        # -------------------------------------------------
        # 9. Rerank final candidates
        # -------------------------------------------------

        if (
            self.reranker is not None
            and hybrid_results
        ):
            return self.reranker.rerank(
                question=question,
                results=hybrid_results,
                top_k=top_k,
            )

        # -------------------------------------------------
        # 10. Return hybrid results if reranker disabled
        # -------------------------------------------------

        return hybrid_results[:top_k]

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _build_filter(
        self,
        access_context: AccessContext | None,
    ) -> RetrievalFilter:
        """
        Convert trusted user access information into
        database retrieval constraints.

        Important:
        Authorization is applied during retrieval,
        not after documents have already been retrieved.
        """

        # ---------------------------------------------
        # No access context
        #
        # Default to public documents only.
        # ---------------------------------------------

        if access_context is None:
            return RetrievalFilter(
                department=None,
                include_public=True,
                active_versions_only=True,
            )

        # ---------------------------------------------
        # Admin
        #
        # Current RetrievalFilter supports department
        # and public visibility.
        #
        # More advanced unrestricted/admin filtering
        # can be added later.
        # ---------------------------------------------

        if access_context.is_admin:
            return RetrievalFilter(
                department=access_context.department,
                include_public=True,
                active_versions_only=True,
            )

        # ---------------------------------------------
        # Normal employee
        #
        # Allowed:
        # - public documents
        # - documents belonging to their department
        # ---------------------------------------------

        return RetrievalFilter(
            department=access_context.department,
            include_public=True,
            active_versions_only=True,
        )

    def _convert_vector_results(
        self,
        rows,
    ) -> list[RetrievalResult]:
        """
        Convert database vector-search rows into our
        standard RetrievalResult objects.
        """

        results: list[RetrievalResult] = []

        for row in rows:

            # -------------------------------------------------
            # Case 1:
            # vector_store.search() already returns
            # RetrievalResult objects.
            # -------------------------------------------------

            if isinstance(
                row,
                RetrievalResult,
            ):
                results.append(row)
                continue

            # -------------------------------------------------
            # Case 2:
            # vector_store returns dictionary rows.
            # -------------------------------------------------

            metadata = dict(
                row.get("metadata") or {}
            )

            score = float(
                row.get(
                    "score",
                    row.get(
                        "similarity",
                        0.0,
                    ),
                )
            )

            # Keep original semantic score.
            #
            # Later:
            # HybridFusion adds rrf_score
            # Reranker adds reranker_score
            metadata["vector_score"] = score

            result = RetrievalResult(
                chunk_id=row.get(
                    "id",
                    row.get("chunk_id"),
                ),
                document_id=row[
                    "document_id"
                ],
                document_version_id=row[
                    "document_version_id"
                ],
                document_name=row[
                    "document_name"
                ],
                chunk_index=row[
                    "chunk_index"
                ],
                content=row[
                    "content"
                ],
                page_number=row.get(
                    "page_number"
                ),
                score=score,
                metadata=metadata,
            )

            results.append(result)

        return results