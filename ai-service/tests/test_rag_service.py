from src.embeddings.embedder import Embedder
from src.llm.mock_llm import MockLLMClient
from src.prompts.prompt_builder import PromptBuilder
from src.rag_service import RAGService
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import (
    PostgresVectorStore,
)


def test_rag_service():

    # -----------------------------------------
    # Create dependencies
    # -----------------------------------------

    embedder = Embedder()

    vector_store = (
        PostgresVectorStore()
    )

    retriever = Retriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    context_builder = (
        ContextBuilder()
    )

    prompt_builder = (
        PromptBuilder()
    )

    llm_client = (
        MockLLMClient()
    )

    # -----------------------------------------
    # Create RAG service
    # -----------------------------------------

    rag_service = RAGService(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        llm_client=llm_client,
    )

    # -----------------------------------------
    # Ask question
    # -----------------------------------------

    question = (
        "Can employees work remotely?"
    )

    result = rag_service.answer(
        question=question,
        top_k=3,
        similarity_threshold=0.5,
    )

    # -----------------------------------------
    # Display result
    # -----------------------------------------

    print("\n")
    print("=" * 70)
    print("QUESTION")
    print("=" * 70)

    print(question)

    print("\n")
    print("=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(result["answer"])

    print("\n")
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for source in result["sources"]:

        print(
            f"Document: "
            f"{source['document_name']}"
        )

        print(
            f"Version: "
            f"{source['document_version_id']}"
        )

        print(
            f"Page: "
            f"{source['page_number']}"
        )

        print(
            f"Score: "
            f"{source['score']:.4f}"
        )

        print("-" * 40)

    # -----------------------------------------
    # Assertions
    # -----------------------------------------

    assert result["answer"]

    assert result["sources"]

    assert (
        "MOCK LLM RESPONSE"
        in result["answer"]
    )