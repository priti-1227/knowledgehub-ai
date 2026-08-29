from src.llm.config import LLMConfig
from src.llm.llm_client import LLMClient
from src.llm.mock_llm import MockLLMClient
from src.llm.providers.local_llm import LocalLLMClient


def create_llm_client(
    config: LLMConfig,
) -> LLMClient:

    provider = config.provider.lower()

    if provider == "mock":

        return MockLLMClient()

    if provider == "local":

        if not config.model:
            raise ValueError(
                "LLM_MODEL is required "
                "for local provider."
            )

        if not config.base_url:
            raise ValueError(
                "LLM_BASE_URL is required "
                "for local provider."
            )

        return LocalLLMClient(
            model=config.model,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )