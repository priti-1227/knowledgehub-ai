import json
from collections import defaultdict
from pathlib import Path

from src.api.dependencies import get_rag_service
from src.security.access_context import AccessContext


DATASET_PATH = (
    Path(__file__).parent
    / "data"
    / "enterprise_eval.json"
)


def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_enterprise_rag_evaluation():

    rag = get_rag_service()

    dataset = load_dataset()

    metrics = {
        "total": 0,
        "answerability_correct": 0,
        "source_correct": 0,
        "answer_content_correct": 0,
        "authorization_correct": 0,
    }

    category_results = defaultdict(
        lambda: {
            "total": 0,
            "passed": 0,
        }
    )

    failures = []

    for item in dataset:

        metrics["total"] += 1

        category = item["category"]

        category_results[
            category
        ]["total"] += 1

        user = AccessContext(
            user_id=(
                f"test-{item['user_department']}"
            ),
            department=item[
                "user_department"
            ],
            roles=("EMPLOYEE",),
            is_admin=False,
        )

        result = rag.answer(
            question=item["question"],
            top_k=3,
            similarity_threshold=0.5,
            access_context=user,
        )

        sources = result.get(
            "sources",
            [],
        )

        source_names = [
            source["document_name"]
            for source in sources
        ]

        # -----------------------------------------
        # Answerability
        # -----------------------------------------

        expected_grounded = (
            item["should_answer"]
        )

        answerability_ok = (
            result["grounded"]
            == expected_grounded
        )

        if answerability_ok:
            metrics[
                "answerability_correct"
            ] += 1

        # -----------------------------------------
        # Source correctness
        # -----------------------------------------

        source_ok = True

        if item["should_answer"]:

            expected_docs = item.get(
                "expected_documents",
                [],
            )

            source_ok = any(
                source
                in expected_docs
                for source in source_names
            )

        if source_ok:
            metrics[
                "source_correct"
            ] += 1

        # -----------------------------------------
        # Authorization leakage
        # -----------------------------------------

        forbidden = item.get(
            "forbidden_documents",
            [],
        )

        authorization_ok = all(
            source not in source_names
            for source in forbidden
        )

        if authorization_ok:
            metrics[
                "authorization_correct"
            ] += 1

        # -----------------------------------------
        # Answer content
        # -----------------------------------------

        answer_ok = True

        expected_terms = item.get(
            "expected_answer_any",
            [],
        )

        if (
            item["should_answer"]
            and expected_terms
        ):

            answer_text = (
                result["answer"]
                .lower()
            )

            answer_ok = any(
                term.lower()
                in answer_text
                for term in expected_terms
            )

        if answer_ok:
            metrics[
                "answer_content_correct"
            ] += 1

        # -----------------------------------------
        # Overall case
        # -----------------------------------------

        case_passed = (
            answerability_ok
            and source_ok
            and authorization_ok
            and answer_ok
        )

        if case_passed:
            category_results[
                category
            ]["passed"] += 1

        else:
            failures.append({
                "id": item["id"],
                "category": category,
                "question": item[
                    "question"
                ],
                "grounded": result[
                    "grounded"
                ],
                "reason": result.get(
                    "grounding_reason"
                ),
                "sources": source_names,
                "answer": result[
                    "answer"
                ],
                "answerability_ok":
                    answerability_ok,
                "source_ok":
                    source_ok,
                "authorization_ok":
                    authorization_ok,
                "answer_ok":
                    answer_ok,
            })

    total = metrics["total"]

    print("\n")
    print("=" * 70)
    print("ENTERPRISE RAG EVALUATION")
    print("=" * 70)

    print(
        "Answerability Accuracy:",
        round(
            metrics[
                "answerability_correct"
            ] / total,
            3,
        ),
    )

    print(
        "Source Accuracy:",
        round(
            metrics[
                "source_correct"
            ] / total,
            3,
        ),
    )

    print(
        "Answer Content Accuracy:",
        round(
            metrics[
                "answer_content_correct"
            ] / total,
            3,
        ),
    )

    print(
        "Authorization Safety:",
        round(
            metrics[
                "authorization_correct"
            ] / total,
            3,
        ),
    )

    print("\nCATEGORY RESULTS")

    for category, values in (
        category_results.items()
    ):

        accuracy = (
            values["passed"]
            / values["total"]
        )

        print(
            category,
            ":",
            f"{values['passed']}"
            f"/{values['total']}",
            f"({accuracy:.2f})",
        )

    if failures:

        print("\n")
        print("=" * 70)
        print("FAILURE ANALYSIS")
        print("=" * 70)

        for failure in failures:

            print("\n---")

            for key, value in (
                failure.items()
            ):
                print(
                    f"{key}: {value}"
                )

    # Baseline evaluation.
    #
    # Don't enforce an artificial accuracy target yet.
    # First collect real baseline metrics.

    assert total > 0