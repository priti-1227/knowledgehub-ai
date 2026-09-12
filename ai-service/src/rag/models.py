from enum import Enum


class AnswerStatus(str, Enum):
    ANSWERED = "answered"

    ANSWERED_WITH_CONFLICT = (
        "answered_with_conflict"
    )

    CONFLICT = "conflict"

    NOT_FOUND = "not_found"