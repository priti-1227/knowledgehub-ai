import json
from pathlib import Path

from src.embeddings.embedder import Embedder
from src.retrieval.reranker import Reranker
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


def test_reranker_thresholds():

    retriever = Retriever(
        embedder=Embedder(),
        vector_store=PostgresVectorStore(),
        reranker=Reranker(),
    )

    dataset = load_dataset()
    for item in dataset:
        print(
            item["question"],
            "-> should_answer:",
            item.get("should_answer"),
        )
    print("\nTOTAL DATASET ITEMS:", len(dataset))

    print(
        "UNSUPPORTED ITEMS:",
        sum(
            1
            for item in dataset
            if not item["should_answer"]
        )
    )

    thresholds = [
   0.0
    ]

    for threshold in thresholds:

        answerable_total = 0
        answerable_accepted = 0

        unsupported_total = 0
        unsupported_rejected = 0

        for item in dataset:

            results = retriever.retrieve(
                question=item["question"],
                top_k=3,
                candidate_k=10,
                similarity_threshold=0.5,
            )

            best_score = (
                results[0].score
                if results
                else float("-inf")
            )
            if not item["should_answer"]:

                print("\nUNSUPPORTED QUESTION:")
                print(item["question"])

                if results:
                    print(
                        "Top result:",
                        results[0].document_name
                    )

                    print(
                        "Reranker score:",
                        round(results[0].score, 4)
                    )

                    print(
                        "Vector score:",
                        round(
                            results[0].metadata.get(
                                "vector_score",
                                0,
                            ),
                            4,
                        )
                    )

            if item["should_answer"]:

                answerable_total += 1

                if best_score >= threshold:
                    answerable_accepted += 1

            else:

                unsupported_total += 1

                if best_score < threshold:
                    unsupported_rejected += 1

        answerable_acceptance = (
            answerable_accepted
            / answerable_total
            if answerable_total
            else 0
        )

        unsupported_rejection = (
            unsupported_rejected
            / unsupported_total
            if unsupported_total
            else 0
        )

        print("\n")
        print("=" * 70)
        print(
            f"RERANKER THRESHOLD: {threshold:.2f}"
        )
        print("=" * 70)

        print(
            "Answerable Acceptance Rate:",
            f"{answerable_acceptance:.2f}"
        )

        print(
            "Unsupported Rejection Rate:",
            f"{unsupported_rejection:.2f}"
        )