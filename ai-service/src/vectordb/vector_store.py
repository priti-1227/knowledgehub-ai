from src.utils.database import get_connection
import json

class PostgresVectorStore:
    """
    PostgreSQL + pgvector based vector store.

    Responsible for storing chunks and embeddings
    and performing vector similarity searches.
    """

    def add(
        self,
        documents: list[dict],
        embeddings: list[list[float]],
    ) -> None:

        if len(documents) != len(embeddings):
            raise ValueError(
                "Number of documents must match "
                "number of embeddings."
            )

        with get_connection() as connection:

            with connection.cursor() as cursor:

                for document, embedding in zip(
                    documents,
                    embeddings,
                ):

                    cursor.execute(
    """
    INSERT INTO document_chunks (
        document_id,
        document_version_id,
        document_name,
        chunk_index,
        content,
        embedding,
        page_number,
        metadata
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s::vector,
        %s,
        %s::jsonb
    )
    """,
    (
        document["document_id"],
        document["document_version_id"],
        document["document_name"],
        document["chunk_index"],
        document["content"],
        str(embedding),
        document.get("page_number"),
        json.dumps(
            document.get("metadata", {})
        ),
    ),
)

            connection.commit()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        similarity_threshold: float = 0.5,
    ) -> list[dict]:

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        if not 0 <= similarity_threshold <= 1:
            raise ValueError(
                "similarity_threshold must be between 0 and 1."
            )

        embedding_text = str(query_embedding)

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        dc.id,
                        dc.document_id,
                        dc.document_version_id,
                        dc.document_name,
                        dc.chunk_index,
                        dc.content,
                        dc.page_number,
                        dc.metadata,

                        1 - (
                            dc.embedding <=> %s::vector
                        ) AS score

                    FROM document_chunks dc

                    JOIN document_versions dv
                        ON dc.document_version_id = dv.id

                    WHERE dv.status = 'active'

                    AND (
                        1 - (
                            dc.embedding <=> %s::vector
                        )
                    ) >= %s

                    ORDER BY dc.embedding <=> %s::vector

                    LIMIT %s
                    """,
                    (
                        embedding_text,
                        embedding_text,
                        similarity_threshold,
                        embedding_text,
                        top_k,
                    ),
                )

                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "document_version_id": row[2],
                "document_name": row[3],
                "chunk_index": row[4],
                "content": row[5],
                "page_number": row[6],
                "metadata": row[7],
                "score": float(row[8]),
            }
            for row in rows
        ]