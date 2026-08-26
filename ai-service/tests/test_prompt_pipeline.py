from src.embeddings.embedder import Embedder
from src.prompts.prompt_builder import PromptBuilder
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import (
    PostgresVectorStore,
)


def test_prompt_pipeline():

    question = (
        "Can employees work remotely?"
    )

    # -----------------------------------------
    # 1. Retrieve
    # -----------------------------------------

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    results = retriever.retrieve(
        question=question,
        top_k=3,
        similarity_threshold=0.5,
    )

    assert results

    # -----------------------------------------
    # 2. Build context
    # -----------------------------------------

    context_builder = ContextBuilder()

    context = context_builder.build(
        results
    )

    assert context

    # -----------------------------------------
    # 3. Build prompt
    # -----------------------------------------

    prompt_builder = PromptBuilder()

    prompts = prompt_builder.build(
        question=question,
        context=context,
    )

    # -----------------------------------------
    # 4. Display
    # -----------------------------------------

    print("\n")
    print("=" * 70)
    print("SYSTEM PROMPT")
    print("=" * 70)

    print(prompts["system"])

    print("\n")
    print("=" * 70)
    print("USER PROMPT")
    print("=" * 70)

    print(prompts["user"])

    # -----------------------------------------
    # Assertions
    # -----------------------------------------

    assert "KnowledgeHub AI" in prompts["system"]

    assert question in prompts["user"]

    assert "Work From Home" in prompts["user"]