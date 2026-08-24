from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Converts text into numerical vectors using a
    Sentence Transformer embedding model.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """
        Convert a single piece of text into an embedding.
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Convert multiple document chunks into embeddings.
        """
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """
        Convert a user question into an embedding.
        """
        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()