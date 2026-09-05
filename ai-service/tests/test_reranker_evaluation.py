import json
from pathlib import Path

from src.embeddings.embedder import Embedder
from src.retrieval.reranker import Reranker
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import (
    PostgresVectorStore,
)


DATASET_PATH = (
    Path(__file__).parent
    / "data"
    / "retrieval_eval.json"
)


def load_dataset():
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_reranker_evaluation():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
        reranker=Reranker(),
    )

    dataset = load_dataset()

    answerable_total = 0
    top1_hits = 0

    for item in dataset:

        if not item["should_answer"]:
            continue

        answerable_total += 1

        results = retriever.retrieve(
            question=item["question"],

            # Final results
            top_k=3,

            # Broad vector retrieval
            candidate_k=10,

            similarity_threshold=0.5,
        )

        print("\n")
        print("=" * 70)
        print("QUESTION")
        print(item["question"])

        print("\nRERANKED RESULTS")

        for result in results:

            print(
                result.document_name,
                "| reranker:",
                round(result.score, 4),
                "| vector:",
                round(
                    result.metadata.get(
                        "vector_score",
                        0,
                    ),
                    4,
                ),
            )

        if results:
            expected_documents = item[
    "expected_documents"
]
            if (
                results
                and results[0].document_name
                in expected_documents
            ):
                top1_hits += 1

    top1_accuracy = (
        top1_hits / answerable_total
        if answerable_total
        else 0
    )

    print("\n")
    print("=" * 70)
    print("RERANKER METRICS")
    print("=" * 70)

    print(
        f"Top-1 Accuracy: "
        f"{top1_accuracy:.2f}"
    )

    assert top1_accuracy >= 0.7