from src.llm.llm_client import LLMClient
from src.prompts.prompt_builder import PromptBuilder
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.grounding import GroundingValidator
from src.retrieval.retriever import Retriever
from src.security.access_context import AccessContext


class RAGService:
    """
    Coordinates retrieval, grounding validation,
    prompt construction, generation and source reporting.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
        grounding_validator: GroundingValidator,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client
        self.grounding_validator = grounding_validator

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
        # 2. Validate whether evidence is strong enough
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
                "grounding_reason": grounding.reason,
                "best_score": grounding.best_score,
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
        # 3. Build context
        # ------------------------------------------------

        context = self.context_builder.build(
            results
        )

        # ------------------------------------------------
        # 4. Build LLM prompt
        # ------------------------------------------------

        prompts = self.prompt_builder.build(
            question=question,
            context=context,
        )

        # ------------------------------------------------
        # 5. Generate answer
        # ------------------------------------------------

        llm_response = self.llm_client.generate(
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

        # ------------------------------------------------
        # 6. Build citations/source metadata
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

        # ------------------------------------------------
        # 7. Standard response
        # ------------------------------------------------

        return {
            "answer": llm_response.content,
            "grounded": True,
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
            "sources": sources,
        }