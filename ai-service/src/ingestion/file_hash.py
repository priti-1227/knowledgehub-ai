import hashlib
from pathlib import Path


def calculate_file_hash(
    file_path: str,
) -> str:
    """
    Calculate SHA-256 hash of a file.

    The same file produces the same hash.
    A changed file produces a different hash.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    sha256 = hashlib.sha256()

    with path.open("rb") as file:

        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()