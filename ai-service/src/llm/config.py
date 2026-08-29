from dataclasses import dataclass
import os


@dataclass(frozen=True)
class LLMConfig:

    provider: str = os.getenv(
        "LLM_PROVIDER",
        "mock",
    )

    model: str = os.getenv(
        "LLM_MODEL",
        "mock-model",
    )

    base_url: str = os.getenv(
        "LLM_BASE_URL",
        "",
    )

    temperature: float = float(
        os.getenv(
            "LLM_TEMPERATURE",
            "0.0",
        )
    )

    max_tokens: int = int(
        os.getenv(
            "LLM_MAX_TOKENS",
            "1000",
        )
    )

    timeout: int = int(
        os.getenv(
            "LLM_TIMEOUT",
            "120",
        )
    )