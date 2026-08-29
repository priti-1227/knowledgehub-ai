from src.llm.config import LLMConfig
from src.llm.llm_client import LLMResponse
from src.llm.llm_factory import create_llm_client


def test_llm_factory():

    config = LLMConfig(
        provider="mock",
        model="mock-model",
    )

    client = create_llm_client(config)

    response = client.generate(
        system_prompt="You are helpful.",
        user_prompt="What is RAG?",
    )

    assert isinstance(
        response,
        LLMResponse,
    )

    assert response.content

    assert response.provider == "mock"

    assert response.model == "mock-model"