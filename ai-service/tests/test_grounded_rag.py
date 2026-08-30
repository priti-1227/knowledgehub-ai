from src.embeddings.embedder import Embedder
from src.llm.config import LLMConfig
from src.llm.llm_factory import create_llm_client
from src.prompts.prompt_builder import PromptBuilder
from src.rag_service import RAGService
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.grounding import GroundingValidator
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import PostgresVectorStore


def create_rag_service() -> RAGService:

    config = LLMConfig(
        provider="local",
        model="llama3.2:3b",
        base_url="http://localhost:11434",
    )

    llm_client = create_llm_client(
        config
    )

    return RAGService(
        retriever=Retriever(
            embedder=Embedder(),
            vector_store=PostgresVectorStore(),
        ),

        context_builder=ContextBuilder(),

        prompt_builder=PromptBuilder(),

        llm_client=llm_client,

        grounding_validator=GroundingValidator(
            minimum_score=0.55
        ),
    )


def test_supported_question():

    rag = create_rag_service()

    question = (
        "Can employees work remotely?"
    )

    result = rag.answer(
        question=question,
        top_k=3,
        similarity_threshold=0.5,
    )

    print("\n")
    print("=" * 70)
    print("SUPPORTED QUESTION")
    print("=" * 70)

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nGrounded:")
    print(result["grounded"])

    print("\nBest Score:")
    print(result["best_score"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            source["document_name"],
            "| Page:",
            source["page_number"],
            "| Score:",
            round(source["score"], 4),
        )

    assert result["grounded"] is True

    assert result["sources"]

    assert result["answer"]


def test_unsupported_question():

    rag = create_rag_service()

    question = (
        "What is the company's maternity "
        "leave policy?"
    )

    result = rag.answer(
        question=question,
        top_k=3,

        # Intentionally stronger threshold
        # for unsupported-question test
        similarity_threshold=0.65,
    )

    print("\n")
    print("=" * 70)
    print("UNSUPPORTED QUESTION")
    print("=" * 70)

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nGrounded:")
    print(result["grounded"])

    print("\nReason:")
    print(result["grounding_reason"])

    assert result["grounded"] is False

    assert (
        "could not find"
        in result["answer"].lower()
    )

    assert result["sources"] == []