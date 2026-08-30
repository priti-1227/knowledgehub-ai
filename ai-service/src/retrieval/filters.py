from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalFilter:
    """
    Defines restrictions applied to vector search.
    """

    department: str | None = None

    include_public: bool = True

    active_versions_only: bool = True