from dataclasses import dataclass
from enum import Enum

from src.llm.llm_client import LLMClient
from src.retrieval.models import RetrievalResult


class ConflictLevel(str, Enum):
    NONE = "none"
    PARTIAL = "partial"
    FULL = "full"


@dataclass
class EvidenceAnalysis:
    can_answer: bool
    conflict_level: ConflictLevel
    reason: str


class EvidenceAnalyzer:

    def __init__(
        self,
        llm_client: LLMClient,
    ):
        self.llm_client = llm_client

    def analyze(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> EvidenceAnalysis:

        if not results:
            return EvidenceAnalysis(
                can_answer=False,
                conflict_level=ConflictLevel.NONE,
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
You are the evidence decision component of an
enterprise RAG system.

You DO NOT answer the user's question.

Determine two things:

1. Does the supplied evidence contain enough information
   to answer the user's actual question?

2. If it does, do the relevant sources conflict?

ANSWERABILITY:

SUPPORTED
- At least one source explicitly contains information
  needed to answer the question.

UNSUPPORTED
- The retrieved sources are only topically related,
  but do not contain the requested information.

Important:
Topical similarity is NOT sufficient.

Example:

Question:
What is the maternity leave duration?

Document:
Employees may work remotely two days per week.

Result:
UNSUPPORTED

The document is an HR policy, but contains no maternity
leave information.

Example:

Question:
Who approves remote work?

Document:
Remote work requires approval from the employee's
reporting manager.

Result:
SUPPORTED


CONFLICT:

NONE
- Relevant sources agree.

PARTIAL
- Sources agree on the main answer but disagree on
  an important detail.

FULL
- Sources directly disagree on the main answer.

Do NOT create conflicts from missing information.

Return EXACTLY two lines:

ANSWERABILITY=SUPPORTED

CONFLICT=NONE

Valid conflict values:
NONE
PARTIAL
FULL
""".strip()

        user_prompt = f"""
QUESTION:

{question}

RETRIEVED DOCUMENT EVIDENCE:

{context}

CLASSIFY THE EVIDENCE.
""".strip()

        response = self.llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        text = (
            response.content
            .strip()
            .upper()
        )

        can_answer = (
            "ANSWERABILITY=SUPPORTED"
            in text
        )

        if "CONFLICT=FULL" in text:
            conflict_level = (
                ConflictLevel.FULL
            )

        elif "CONFLICT=PARTIAL" in text:
            conflict_level = (
                ConflictLevel.PARTIAL
            )

        else:
            conflict_level = (
                ConflictLevel.NONE
            )

        return EvidenceAnalysis(
            can_answer=can_answer,
            conflict_level=conflict_level,
            reason=(
                "sufficient_evidence"
                if can_answer
                else "insufficient_evidence"
            ),
        )