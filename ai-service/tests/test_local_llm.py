from src.llm.config import LLMConfig
from src.llm.llm_factory import create_llm_client


def test_local_llm():

    config = LLMConfig(
        provider="local",
        model="llama3.2:3b",
        base_url="http://localhost:11434",
    )

    llm = create_llm_client(config)

    response = llm.generate(
        system_prompt=(
            "Answer clearly and briefly."
        ),
        user_prompt=(
            "What is RAG?"
        ),
    )

    print("\n")
    print("=" * 70)
    print("LOCAL LLM")
    print("=" * 70)

    print(response.content)

    print("\nProvider:", response.provider)
    print("Model:", response.model)

    assert response.content
    assert response.provider == "local"
    assert response.model == "llama3.2:3b"