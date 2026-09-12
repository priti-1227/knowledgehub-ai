from dataclasses import dataclass

from src.llm.llm_client import LLMClient
from src.retrieval.models import RetrievalResult


@dataclass
class EvidenceDecision:
    can_answer: bool
    reason: str


class EvidenceVerifier:

    def __init__(
        self,
        llm_client: LLMClient,
    ):
        self.llm_client = llm_client

    def verify(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> EvidenceDecision:

        if not results:
            return EvidenceDecision(
                can_answer=False,
                reason="no_retrieved_evidence",
            )

        context = "\n\n".join(
            f"""
SOURCE {index}: {result.document_name}

{result.content}
""".strip()
            for index, result in enumerate(
                results,
                start=1,
            )
        )

        system_prompt = """
You are a binary evidence classifier for a RAG system.

Your job is ONLY to decide whether the supplied documents
contain information that can answer the user's question.

Return:

SUPPORTED

when at least one supplied document contains a direct answer
to the question.

Return:

UNSUPPORTED

only when none of the supplied documents contains the
information needed to answer the question.

IMPORTANT:

Conflicting details do NOT mean the question is unsupported.

Example:

Question:
Can employees work remotely?

Source A:
Employees may work remotely two days per week.

Source B:
Employees may work remotely three days per week.

Classification:
SUPPORTED

Reason:
Both sources directly establish that remote work is allowed.
The difference in the number of days is a conflict that will
be handled separately.

Another example:

Question:
What is the maternity leave policy?

Source:
Employees may work remotely two days per week.

Classification:
UNSUPPORTED

Do not answer the user's question.
Do not explain your classification.

Return exactly one word:

SUPPORTED

or

UNSUPPORTED
""".strip()

        user_prompt = f"""
QUESTION:

{question}

DOCUMENTS:

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

        print("\nEVIDENCE VERIFIER")
        print("Question:", question)
        print("Raw decision:", decision)

        # Exact classification instead of loose parsing.
        first_line = (
            decision.splitlines()[0]
            .strip()
        )

        if first_line == "SUPPORTED":
            return EvidenceDecision(
                can_answer=True,
                reason="evidence_supported",
            )

        return EvidenceDecision(
            can_answer=False,
            reason="insufficient_evidence",
        )