from dataclasses import dataclass, asdict


@dataclass
class RetrievalDiagnostic:
    chunk_id: str | int
    document_name: str

    vector_score: float | None
    rrf_score: float | None
    reranker_score: float | None

    page_number: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def build_retrieval_diagnostics(
    results,
) -> list[dict]:

    diagnostics = []

    for result in results:

        metadata = result.metadata or {}

        diagnostic = RetrievalDiagnostic(
            chunk_id=result.chunk_id,
            document_name=result.document_name,

            vector_score=metadata.get(
                "vector_score"
            ),

            rrf_score=metadata.get(
                "rrf_score"
            ),

            reranker_score=metadata.get(
                "reranker_score"
            ),

            page_number=result.page_number,
        )

        diagnostics.append(
            diagnostic.to_dict()
        )

    return diagnostics