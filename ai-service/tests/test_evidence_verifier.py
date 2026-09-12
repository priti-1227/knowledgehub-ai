from src.api.dependencies import get_rag_service
from src.security.access_context import AccessContext


def test_supported_and_unsupported_questions():

    rag = get_rag_service()

    user = AccessContext(
        user_id=101,
        department="HR",
        roles=("employee",),
        is_admin=False,
    )

    supported = rag.answer(
        question="Can employees work remotely?",
        top_k=3,
        similarity_threshold=0.5,
        access_context=user,
    )

    print("\n")
    print("=" * 70)
    print("SUPPORTED")
    print("=" * 70)

    print(supported["answer"])
    print(
        "Grounded:",
        supported["grounded"]
    )

    unsupported = rag.answer(
        question=(
            "What is the maternity leave policy?"
        ),
        top_k=3,
        similarity_threshold=0.5,
        access_context=user,
    )

    print("\n")
    print("=" * 70)
    print("UNSUPPORTED")
    print("=" * 70)

    print(unsupported["answer"])

    print(
        "Grounded:",
        unsupported["grounded"]
    )

    print(
        "Reason:",
        unsupported["grounding_reason"]
    )

    assert supported["grounded"] is True

    assert unsupported["grounded"] is False

    assert (
        unsupported["grounding_reason"]
        == "insufficient_evidence"
    )