import requests

from src.llm.llm_client import (
    LLMClient,
    LLMResponse,
)


class LocalLLMClient(LLMClient):
    """
    Local LLM provider.

    Communicates with a local inference server
    through HTTP.

    The rest of KnowledgeHub does not depend
    directly on Ollama.
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

        payload = {
            "model": self.model,

            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            "stream": False,
        }

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not content:
            raise RuntimeError(
                "Local LLM returned an empty response."
            )

        return LLMResponse(
            content=content,
            model=self.model,
            provider="local",
        )