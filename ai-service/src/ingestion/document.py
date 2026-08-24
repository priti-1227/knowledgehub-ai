from dataclasses import dataclass, field


@dataclass
class Document:
    """
    Represents a source document before chunking.
    """

    content: str
    source: str
    metadata: dict = field(default_factory=dict)