from src.llm.llm_client import LLMClient
from src.prompts.prompt_builder import PromptBuilder
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.grounding import GroundingValidator
from src.retrieval.retriever import Retriever
from src.security.access_context import AccessContext
from src.retrieval.diagnostics import (
    build_retrieval_diagnostics,
)

from src.retrieval.evidence_verifier import (
    EvidenceVerifier,
)

from src.retrieval.conflict_detector import (
    ConflictDetector,
    ConflictLevel,
)

from src.rag.models import AnswerStatus


class RAGService:
    """
    Coordinates retrieval, grounding validation,
    evidence verification, conflict detection,
    prompt construction, generation and source reporting.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
        grounding_validator: GroundingValidator,
        evidence_verifier: EvidenceVerifier,
        conflict_detector: ConflictDetector,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.grounding_validator = grounding_validator
        self.evidence_verifier = evidence_verifier
        self.conflict_detector = conflict_detector

    def answer(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        access_context: AccessContext | None = None,
    ) -> dict:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # ------------------------------------------------
        # 1. Retrieve candidate evidence
        # ------------------------------------------------

        results = self.retriever.retrieve(
            question=question,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
            access_context=access_context,
        )

        # ------------------------------------------------
        # 2. Grounding check
        # ------------------------------------------------

        grounding = self.grounding_validator.validate(
            results
        )

        if not grounding.can_answer:
            return {
                "answer": (
                    "I could not find this information "
                    "in the available documents."
                ),

                "grounded": False,

                "answer_status":
                    AnswerStatus.NOT_FOUND,

                "conflict": {
                    "has_conflict": False,
                    "level": "none",
                    "reason": "no_evidence",
                },

                "grounding_reason":
                    grounding.reason,

                "best_score":
                    grounding.best_score,

                "model": None,

                "provider": None,

                "usage": {
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                },

                "sources": [],
            }

        # ------------------------------------------------
        # 3. Evidence verification
        # ------------------------------------------------

        evidence = self.evidence_verifier.verify(
            question=question,
            results=results,
        )

        if not evidence.can_answer:
            return {
                "answer": (
                    "I could not find this information "
                    "in the available documents."
                ),

                "grounded": False,

                "answer_status":
                    AnswerStatus.NOT_FOUND,

                "conflict": {
                    "has_conflict": False,
                    "level": "none",
                    "reason": "insufficient_evidence",
                },

                "grounding_reason":
                    evidence.reason,

                "best_score": (
                    results[0].score
                    if results
                    else None
                ),

                "model": None,

                "provider": None,

                "usage": {
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                },

                "sources": [],
            }

        # ------------------------------------------------
        # 4. Conflict detection
        # ------------------------------------------------

        conflict = self.conflict_detector.detect(
            question=question,
            results=results,
        )

        # ------------------------------------------------
        # 5. Build context
        # ------------------------------------------------

        context = self.context_builder.build(
            results
        )

        # ------------------------------------------------
        # 6. Build prompt
        # ------------------------------------------------

        prompts = self.prompt_builder.build(
            question=question,
            context=context,
        )

        # ------------------------------------------------
        # 7. Generate answer
        # ------------------------------------------------

        llm_response = self.llm_client.generate(
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

        # ------------------------------------------------
        # 8. Build source metadata
        # ------------------------------------------------

        sources = [
            {
                "chunk_id":
                    result.chunk_id,

                "document_id":
                    result.document_id,

                "document_version_id":
                    result.document_version_id,

                "document_name":
                    result.document_name,

                "page_number":
                    result.page_number,

                "score":
                    result.score,
            }
            for result in results
        ]
        retrieval_diagnostics = (
        build_retrieval_diagnostics(
            results
        )
    )

        # ------------------------------------------------
        # 9. Decide answer status
        # ------------------------------------------------

        if (
            conflict.level
            == ConflictLevel.FULL
        ):
            answer_status = (
                AnswerStatus.CONFLICT
            )

        elif (
            conflict.level
            == ConflictLevel.PARTIAL
        ):
            answer_status = (
                AnswerStatus.ANSWERED_WITH_CONFLICT
            )

        else:
            answer_status = (
                AnswerStatus.ANSWERED
            )

        # ------------------------------------------------
        # 10. Final response
        # ------------------------------------------------

        return {
            "answer":
                llm_response.content,

            "grounded":
                True,

            "answer_status":
                answer_status,

            "conflict": {
                "has_conflict":
                    conflict.has_conflict,

                "level":
                    conflict.level.value,

                "reason":
                    conflict.reason,
            },

            "grounding_reason":
                grounding.reason,

            "best_score":
                grounding.best_score,

            "model":
                llm_response.model,

            "provider":
                llm_response.provider,

            "usage": {
                "prompt_tokens":
                    llm_response.prompt_tokens,

                "completion_tokens":
                    llm_response.completion_tokens,

                "total_tokens":
                    llm_response.total_tokens,
            },

            "sources":
                sources,
            "retrieval_diagnostics":
    retrieval_diagnostics,
    
        }