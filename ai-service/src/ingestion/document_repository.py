from src.utils.database import get_connection


class DocumentRepository:
    """
    Handles document and document-version metadata.
    """

    def create_document(
        self,
        name: str,
        department: str | None = None,
        description: str | None = None,
    ) -> int:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO documents (
                        name,
                        department,
                        description
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (
                        name,
                        department,
                        description,
                    ),
                )

                document_id = cursor.fetchone()[0]

            connection.commit()

        return document_id

    def find_document_by_name(
        self,
        name: str,
    ) -> int | None:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id
                    FROM documents
                    WHERE name = %s
                    LIMIT 1
                    """,
                    (name,),
                )

                row = cursor.fetchone()

        return row[0] if row else None

    def find_version_by_hash(
        self,
        file_hash: str,
    ) -> int | None:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id
                    FROM document_versions
                    WHERE file_hash = %s
                    LIMIT 1
                    """,
                    (file_hash,),
                )

                row = cursor.fetchone()

        return row[0] if row else None

    def get_next_version_number(
        self,
        document_id: int,
    ) -> int:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT COALESCE(
                        MAX(version_number),
                        0
                    ) + 1
                    FROM document_versions
                    WHERE document_id = %s
                    """,
                    (document_id,),
                )

                return cursor.fetchone()[0]

    def create_version(
        self,
        document_id: int,
        version_number: int,
        file_name: str,
        file_path: str,
        file_hash: str,
        status: str = "processing",
    ) -> int:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO document_versions (
                        document_id,
                        version_number,
                        file_name,
                        file_path,
                        file_hash,
                        status
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        document_id,
                        version_number,
                        file_name,
                        file_path,
                        file_hash,
                        status,
                    ),
                )

                version_id = cursor.fetchone()[0]

            connection.commit()

        return version_id

    def update_version_status(
    self,
    version_id: int,
    status: str,
) -> None:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                if status == "active":

                    cursor.execute(
                        """
                        SELECT document_id
                        FROM document_versions
                        WHERE id = %s
                        """,
                        (version_id,),
                    )

                    row = cursor.fetchone()

                    if row is None:
                        raise ValueError(
                            f"Version not found: {version_id}"
                        )

                    document_id = row[0]

                    cursor.execute(
                        """
                        UPDATE document_versions
                        SET status = 'archived'
                        WHERE document_id = %s
                        AND status = 'active'
                        AND id <> %s
                        """,
                        (
                            document_id,
                            version_id,
                        ),
                    )

                cursor.execute(
                    """
                    UPDATE document_versions
                    SET status = %s
                    WHERE id = %s
                    """,
                    (
                        status,
                        version_id,
                    ),
                )

            connection.commit()
    def archive_active_versions(
    self,
    document_id: int,
) -> None:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE document_versions
                    SET status = 'archived'
                    WHERE document_id = %s
                    AND status = 'active'
                    """,
                    (document_id,),
                )

            connection.commit()