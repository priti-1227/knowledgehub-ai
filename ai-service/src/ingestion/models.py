from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentRecord:
    """
    Represents the logical document.

    Example:
        Leave Policy
    """

    id: int
    name: str
    department: Optional[str] = None


@dataclass
class DocumentVersion:
    """
    Represents one uploaded version of a document.

    Example:
        Leave Policy v2
    """

    id: int
    document_id: int
    version_number: int
    file_name: str
    file_hash: Optional[str] = None
    status: str = "active"