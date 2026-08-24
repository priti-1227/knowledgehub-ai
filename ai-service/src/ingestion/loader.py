from pathlib import Path

from src.ingestion.document import Document


class TextLoader:
    """
    Loads a text file and converts it into a Document object.
    """

    def load(self, file_path: str) -> Document:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        content = path.read_text(
            encoding="utf-8"
        )

        return Document(
            content=content,
            source=str(path),
            metadata={
                "filename": path.name,
                "extension": path.suffix,
            },
        )