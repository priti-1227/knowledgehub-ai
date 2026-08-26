from src.llm.llm_client import (
    LLMClient,
    LLMResponse,
)


class MockLLMClient(LLMClient):
    """
    Fake LLM used for testing.
    """

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:

        return LLMResponse(
            content=(
                "MOCK LLM RESPONSE\n\n"
                "The LLM received the provided "
                "document context and question."
            ),
            model="mock-model",
            provider="mock",
        )