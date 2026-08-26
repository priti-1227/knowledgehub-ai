from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """
    Standard response returned by every LLM provider.
    """

    content: str

    model: str

    provider: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None


class LLMClient(ABC):
    """
    Common interface for all LLM providers.

    RAGService depends on this interface rather
    than depending on a specific provider.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        """
        Generate a response from an LLM.
        """

        raise NotImplementedError