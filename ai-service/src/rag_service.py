from time import perf_counter

from src.llm.llm_client import LLMClient
from src.prompts.prompt_builder import PromptBuilder

from src.retrieval.context_builder import ContextBuilder
from src.retrieval.grounding import GroundingValidator
from src.retrieval.retriever import Retriever

from src.retrieval.diagnostics import (
    build_retrieval_diagnostics,
)

from src.retrieval.evidence_analyzer import (
    EvidenceAnalyzer,
    ConflictLevel,
)

from src.security.access_context import AccessContext
from src.rag.models import AnswerStatus


class RAGService:
    """
    Coordinates the complete RAG answering pipeline.

    Current pipeline:

        Question
            ↓
        Permission-aware retrieval
            ↓
        Hybrid retrieval + reranking
            ↓
        Grounding pre-check
            ↓
        Evidence analysis
            ├── answerability
            └── conflict detection
            ↓
        Context construction
            ↓
        Prompt construction
            ↓
        LLM generation
            ↓
        Sources + diagnostics
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
        grounding_validator: GroundingValidator,
        evidence_analyzer: EvidenceAnalyzer,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.grounding_validator = grounding_validator
        self.evidence_analyzer = evidence_analyzer

    def answer(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        access_context: AccessContext | None = None,
    ) -> dict:

        # =================================================
        # 0. Validate input
        # =================================================

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        total_start = perf_counter()

        # =================================================
        # 1. Retrieve candidate evidence
        # =================================================

        retrieval_start = perf_counter()

        results = self.retriever.retrieve(
            question=question,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
            access_context=access_context,
        )

        retrieval_ms = (
            perf_counter()
            - retrieval_start
        ) * 1000

        # =================================================
        # 2. Initial grounding check
        # =================================================

        grounding = (
            self.grounding_validator.validate(
                results
            )
        )

        # -------------------------------------------------
        # No retrieval results / grounding failure
        # -------------------------------------------------

        if not grounding.can_answer:

            total_ms = (
                perf_counter()
                - total_start
            ) * 1000

            self._print_timing(
                retrieval_ms=retrieval_ms,
                analysis_ms=0.0,
                generation_ms=0.0,
                total_ms=total_ms,
            )

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

                "retrieval_diagnostics": [],
            }

        # =================================================
        # 3. Evidence analysis
        # =================================================
        #
        # EvidenceAnalyzer replaces:
        #
        #   EvidenceVerifier
        #       +
        #   ConflictDetector
        #
        # One model call now handles:
        #
        #   - Is the evidence sufficient?
        #   - Do relevant sources conflict?
        #
        # =================================================

        analysis_start = perf_counter()

        analysis = (
            self.evidence_analyzer.analyze(
                question=question,
                results=results,
            )
        )

        analysis_ms = (
            perf_counter()
            - analysis_start
        ) * 1000

        # -------------------------------------------------
        # Retrieved documents exist, but they do not
        # actually contain enough evidence to answer.
        # -------------------------------------------------

        if not analysis.can_answer:

            total_ms = (
                perf_counter()
                - total_start
            ) * 1000

            self._print_timing(
                retrieval_ms=retrieval_ms,
                analysis_ms=analysis_ms,
                generation_ms=0.0,
                total_ms=total_ms,
            )

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
                    "reason":
                        "insufficient_evidence",
                },

                "grounding_reason":
                    analysis.reason,

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

                # Keep these internally useful for
                # debugging unsupported retrieval.
                "retrieval_diagnostics":
                    build_retrieval_diagnostics(
                        results
                    ),
            }

        # =================================================
        # 4. Build verified context
        # =================================================

        context = (
            self.context_builder.build(
                results
            )
        )

        # =================================================
        # 5. Build final answer prompt
        # =================================================

        prompts = (
            self.prompt_builder.build(
                question=question,
                context=context,
            )
        )

        # =================================================
        # 6. Generate answer
        # =================================================

        generation_start = perf_counter()

        llm_response = (
            self.llm_client.generate(
                system_prompt=
                    prompts["system"],

                user_prompt=
                    prompts["user"],
            )
        )

        # =================================================
        # 7. Safety guard
        # =================================================
        #
        # EvidenceAnalyzer has already said that sufficient
        # evidence exists.
        #
        # A small generative model can occasionally still
        # produce a "not found" response.
        #
        # If that happens, regenerate with a stronger,
        # generic grounding instruction.
        # =================================================

        not_found_phrase = (
            "i could not find this information "
            "in the available documents"
        )

        if (
            not_found_phrase
            in llm_response.content.lower()
        ):

            print(
                "\nWARNING:"
                " Generator returned NOT_FOUND "
                "even though evidence was verified."
            )

            corrective_system_prompt = """
You are KnowledgeHub AI.

The supplied evidence has already been verified as
sufficient to answer the user's question.

Answer using ONLY the supplied evidence.

Rules:

1. Answer the user's actual question directly.

2. Do not use outside knowledge.

3. Do not invent facts, requirements, implications,
   exceptions, procedures, permissions, or assumptions.

4. State only what the evidence supports.

5. If a requested detail is not explicitly specified,
   distinguish the supported information from the
   unspecified detail.

6. Do not invent conflicts.

7. Do not say that the information was not found,
   because supporting evidence has already been verified.

8. Keep the answer concise and factual.
""".strip()

            corrective_user_prompt = f"""
VERIFIED DOCUMENT EVIDENCE:

{context}

USER QUESTION:

{question}

Answer directly using only the verified evidence.
""".strip()

            llm_response = (
                self.llm_client.generate(
                    system_prompt=
                        corrective_system_prompt,

                    user_prompt=
                        corrective_user_prompt,
                )
            )

        generation_ms = (
            perf_counter()
            - generation_start
        ) * 1000

        # =================================================
        # 8. Build deduplicated sources
        # =================================================
        #
        # Several chunks may belong to the same document
        # page.
        #
        # Normal users should see one source card per
        # document/page, not duplicate cards.
        # =================================================

        sources = []

        seen_sources = set()

        for result in results:

            source_key = (
                result.document_id,
                result.page_number,
            )

            if source_key in seen_sources:
                continue

            seen_sources.add(
                source_key
            )

            sources.append({
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
            })

        # =================================================
        # 9. Retrieval diagnostics
        # =================================================

        retrieval_diagnostics = (
            build_retrieval_diagnostics(
                results
            )
        )

        # =================================================
        # 10. Determine structured answer status
        # =================================================

        if (
            analysis.conflict_level
            == ConflictLevel.FULL
        ):

            answer_status = (
                AnswerStatus.CONFLICT
            )

            conflict_reason = (
                "core_conflict"
            )

        elif (
            analysis.conflict_level
            == ConflictLevel.PARTIAL
        ):

            answer_status = (
                AnswerStatus.ANSWERED_WITH_CONFLICT
            )

            conflict_reason = (
                "detail_conflict"
            )

        else:

            answer_status = (
                AnswerStatus.ANSWERED
            )

            conflict_reason = (
                "sources_consistent"
            )

        has_conflict = (
            analysis.conflict_level
            != ConflictLevel.NONE
        )

        # =================================================
        # 11. Calculate total latency
        # =================================================

        total_ms = (
            perf_counter()
            - total_start
        ) * 1000

        self._print_timing(
            retrieval_ms=retrieval_ms,
            analysis_ms=analysis_ms,
            generation_ms=generation_ms,
            total_ms=total_ms,
        )

        # =================================================
        # 12. Final response
        # =================================================

        return {
            "answer":
                llm_response.content,

            "grounded":
                True,

            "answer_status":
                answer_status,

            "conflict": {
                "has_conflict":
                    has_conflict,

                "level":
                    analysis.conflict_level.value,

                "reason":
                    conflict_reason,
            },

            "grounding_reason":
                analysis.reason,

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

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    @staticmethod
    def _print_timing(
        retrieval_ms: float,
        analysis_ms: float,
        generation_ms: float,
        total_ms: float,
    ) -> None:

        print("\n")
        print("=" * 60)
        print("RAG TIMING")
        print("=" * 60)

        print(
            "Retrieval:",
            f"{retrieval_ms:.2f} ms",
        )

        print(
            "Evidence analysis:",
            f"{analysis_ms:.2f} ms",
        )

        print(
            "Generation:",
            f"{generation_ms:.2f} ms",
        )

        print(
            "Total:",
            f"{total_ms:.2f} ms",
        )

        print("=" * 60)