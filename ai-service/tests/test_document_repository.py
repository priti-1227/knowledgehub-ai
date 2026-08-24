from src.ingestion.document_repository import (
    DocumentRepository,
)
from src.ingestion.file_hash import (
    calculate_file_hash,
)


def test_document_repository(tmp_path):

    file_path = (
        tmp_path / "leave_policy.pdf"
    )

    file_path.write_bytes(
        b"Leave Policy Version 1"
    )

    file_hash = calculate_file_hash(
        str(file_path)
    )

    assert file_hash

    repository = DocumentRepository()

    document_id = repository.create_document(
        name="Leave Policy",
        department="HR",
        description="Company leave policy",
    )

    assert document_id > 0

    version_id = repository.create_version(
        document_id=document_id,
        version_number=1,
        file_name=file_path.name,
        file_path=str(file_path),
        file_hash=file_hash,
    )

    assert version_id > 0

    print("\nDOCUMENT ID:", document_id)
    print("VERSION ID:", version_id)
    print("FILE HASH:", file_hash)