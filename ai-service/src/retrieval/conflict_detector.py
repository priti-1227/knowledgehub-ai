from dataclasses import dataclass
from enum import Enum

from src.llm.llm_client import LLMClient
from src.retrieval.models import RetrievalResult


class ConflictLevel(str, Enum):
    NONE = "none"
    PARTIAL = "partial"
    FULL = "full"


@dataclass
class ConflictDecision:
    has_conflict: bool
    level: ConflictLevel
    reason: str


class ConflictDetector:

    def __init__(
        self,
        llm_client: LLMClient,
    ):
        self.llm_client = llm_client

    def detect(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> ConflictDecision:

        if len(results) < 2:
            return ConflictDecision(
                has_conflict=False,
                level=ConflictLevel.NONE,
                reason="single_source",
            )

        context = "\n\n".join(
            f"""
SOURCE: {result.document_name}

CONTENT:
{result.content}
""".strip()
            for result in results
        )

        system_prompt = """
You are a document conflict classifier.

Compare the supplied sources only with respect to
the user's question.

Classify the evidence into exactly one category:

CONSISTENT
- The sources agree on the answer.
- One source may contain more detail than another.

PARTIAL_CONFLICT
- The sources agree on the main/core answer,
  but disagree on an important detail such as:
  number, limit, date, duration, requirement,
  procedure, or condition.

FULL_CONFLICT
- The sources give opposite or incompatible answers
  to the main question itself.

Example:

Question:
Can employees work remotely?

Source A:
Employees may work remotely two days per week.

Source B:
Employees may work remotely three days per week.

Classification:
PARTIAL_CONFLICT

Both sources agree that remote work is allowed,
but disagree on the number of days.

Return exactly one value:

CONSISTENT
PARTIAL_CONFLICT
FULL_CONFLICT
""".strip()

        user_prompt = f"""
QUESTION:
{question}

SOURCES:
{context}

CLASSIFICATION:
""".strip()

        response = self.llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        decision = (
            response.content
            .strip()
            .upper()
        )

        if decision.startswith(
            "PARTIAL_CONFLICT"
        ):
            return ConflictDecision(
                has_conflict=True,
                level=ConflictLevel.PARTIAL,
                reason="detail_conflict",
            )

        if decision.startswith(
            "FULL_CONFLICT"
        ):
            return ConflictDecision(
                has_conflict=True,
                level=ConflictLevel.FULL,
                reason="core_conflict",
            )

        return ConflictDecision(
            has_conflict=False,
            level=ConflictLevel.NONE,
            reason="sources_consistent",
        )