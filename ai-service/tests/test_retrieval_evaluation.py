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


def test_retrieval_evaluation():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
    )

    dataset = load_dataset()

    total_answerable = 0
    recall_hits = 0

    top_k = 3

    for item in dataset:

        question = item["question"]

        results = retriever.retrieve(
            question=question,
            top_k=top_k,
            similarity_threshold=0.5,
        )

        print("\n")
        print("=" * 70)
        print("QUESTION")
        print(question)

        print("\nRESULTS")

        for result in results:
            print(
                result.document_name,
                "|",
                round(result.score, 4),
            )

        if not item["should_answer"]:
            continue

        total_answerable += 1

        expected_document = (
            item["expected_document"]
        )

        found = any(
            result.document_name
            == expected_document
            for result in results
        )

        if found:
            recall_hits += 1

    recall_at_k = (
        recall_hits / total_answerable
        if total_answerable
        else 0
    )

    print("\n")
    print("=" * 70)
    print("RETRIEVAL METRICS")
    print("=" * 70)

    print(
        f"Recall@{top_k}: "
        f"{recall_at_k:.2f}"
    )

    assert recall_at_k >= 0.7