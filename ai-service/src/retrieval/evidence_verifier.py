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
You are an evidence-classification component
inside a RAG system.

Your ONLY task is to determine whether at least
one supplied document contains information that
can answer the user's question.

Return exactly:

SUPPORTED

or

UNSUPPORTED


SUPPORTED means:

At least one document explicitly contains the fact,
person, role, number, date, condition, rule,
procedure, permission, or other information needed
to answer the question.

The wording does NOT need to exactly match the
question.


IMPORTANT EXAMPLES:


Example 1:

Question:
Who approves remote work?

Document:
Remote work requires approval from the employee's
reporting manager.

Classification:
SUPPORTED


Example 2:

Question:
How many days can employees work remotely?

Document:
Employees may work remotely up to two days per week.

Classification:
SUPPORTED


Example 3:

Question:
Can employees work remotely?

Document:
Employees may work from home up to three days per week.

Classification:
SUPPORTED


Example 4:

Question:
What is the maternity leave duration?

Document:
Employees may work remotely up to two days per week.

Classification:
UNSUPPORTED


IMPORTANT RULES:

1. Judge only whether evidence exists.

2. Do NOT answer the user's question.

3. Do NOT reject evidence simply because different
   sources contain conflicting details.
   Conflict detection is handled by another component.

4. If one document contains enough information to
   answer the question, return SUPPORTED.

5. Synonyms count as supporting evidence.

Examples:

"reporting manager approval"
supports
"Who approves?"

"work from home"
can support
"remote work"

6. Return UNSUPPORTED only when none of the supplied
   documents contains the information needed.

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
        print("\n" + "=" * 70)
        print("EVIDENCE SENT TO VERIFIER")
        print("=" * 70)

        print("Question:")
        print(question)

        print("\nContext:")
        print(context)
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