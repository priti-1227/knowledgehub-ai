from dataclasses import dataclass

from src.retrieval.models import RetrievalResult


@dataclass
class GroundingDecision:
    """
    Represents whether retrieved evidence is strong
    enough to answer a user's question.
    """

    can_answer: bool
    reason: str
    best_score: float | None
    result_count: int


class GroundingValidator:
    """
    Performs a lightweight evidence-quality check
    before the LLM is allowed to generate an answer.
    """

    def __init__(
        self,
        minimum_score: float = 0.55,
        minimum_results: int = 1,
    ):
        self.minimum_score = minimum_score
        self.minimum_results = minimum_results

    def validate(
        self,
        results: list[RetrievalResult],
    ) -> GroundingDecision:

        if not results:
            return GroundingDecision(
                can_answer=False,
                reason="no_retrieval_results",
                best_score=None,
                result_count=0,
            )

        best_score = max(
            result.score
            for result in results
        )

        if len(results) < self.minimum_results:
            return GroundingDecision(
                can_answer=False,
                reason="insufficient_results",
                best_score=best_score,
                result_count=len(results),
            )

        if best_score < self.minimum_score:
            return GroundingDecision(
                can_answer=False,
                reason="low_similarity",
                best_score=best_score,
                result_count=len(results),
            )

        return GroundingDecision(
            can_answer=True,
            reason="sufficient_evidence",
            best_score=best_score,
            result_count=len(results),
        )