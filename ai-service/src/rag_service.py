from src.llm.llm_client import LLMClient
from src.prompts.prompt_builder import PromptBuilder
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.retriever import Retriever


class RAGService:
    """
    Coordinates the complete Retrieval-Augmented
    Generation workflow.
    """

    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ):

        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def answer(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
    ) -> dict:

        # -----------------------------------------
        # 1. Retrieve relevant documents
        # -----------------------------------------

        results = self.retriever.retrieve(
            question=question,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
        )

        # -----------------------------------------
        # 2. No relevant context
        # -----------------------------------------

        if not results:

            return {
                "answer": (
                    "I couldn't find relevant "
                    "information in the available "
                    "documents."
                ),
                "sources": [],
            }

        # -----------------------------------------
        # 3. Build context
        # -----------------------------------------

        context = (
            self.context_builder.build(
                results
            )
        )

        # -----------------------------------------
        # 4. Build prompts
        # -----------------------------------------

        prompts = self.prompt_builder.build(
            question=question,
            context=context,
        )

        # -----------------------------------------
        # 5. Generate answer
        # -----------------------------------------

        llm_response = self.llm_client.generate(
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )

        # -----------------------------------------
        # 6. Prepare sources
        # -----------------------------------------

        sources = [
            {
                "document_name":
                    result.document_name,

                "document_version_id":
                    result.document_version_id,

                "page_number":
                    result.page_number,

                "score":
                    result.score,

                "chunk_id":
                    result.chunk_id,
            }
            for result in results
        ]

        return {
        "answer": llm_response.content,
        "model": llm_response.model,
        "provider": llm_response.provider,
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