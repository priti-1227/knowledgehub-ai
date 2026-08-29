from src.llm.llm_client import LLMClient, LLMResponse


class LocalLLMClient(LLMClient):
    """
    Adapter for a locally hosted LLM inference server.

    The rest of KnowledgeHub does not need to know
    which local inference engine is being used.
    """

    def __init__(
        self,
        model: str,
        base_url: str,
        timeout: int = 120,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        raise NotImplementedError(
            "Local LLM provider is not connected yet."
        )