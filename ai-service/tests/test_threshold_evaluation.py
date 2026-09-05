import json
from pathlib import Path

from src.embeddings.embedder import Embedder
from src.retrieval.retriever import Retriever
from src.vectordb.vector_store import PostgresVectorStore


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


def test_similarity_thresholds():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    dataset = load_dataset()

    thresholds = [
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
    ]

    for threshold in thresholds:

        answerable_total = 0
        answerable_hits = 0

        unsupported_total = 0
        unsupported_rejected = 0

        for item in dataset:

            results = retriever.retrieve(
                question=item["question"],
                top_k=3,
                similarity_threshold=threshold,
            )

            if item["should_answer"]:

                answerable_total += 1

                expected_document = (
                    item["expected_document"]
                )

                found = any(
                    result.document_name
                    == expected_document
                    for result in results
                )

                if found:
                    answerable_hits += 1

            else:

                unsupported_total += 1

                if not results:
                    unsupported_rejected += 1

        recall = (
            answerable_hits
            / answerable_total
            if answerable_total
            else 0
        )

        rejection_rate = (
            unsupported_rejected
            / unsupported_total
            if unsupported_total
            else 0
        )

        print("\n")
        print("=" * 70)
        print(
            f"THRESHOLD: {threshold:.2f}"
        )
        print("=" * 70)

        print(
            f"Answerable Recall@3: "
            f"{recall:.2f}"
        )

        print(
            f"Unsupported Rejection Rate: "
            f"{rejection_rate:.2f}"
        )