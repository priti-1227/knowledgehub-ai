from src.retrieval.models import RetrievalResult


class ContextBuilder:
    """
    Converts retrieved chunks into structured context
    that can safely be provided to an LLM.
    """

    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:

        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            source = (
                f"{result.document_name}"
            )

            if result.page_number is not None:
                source += (
                    f" | Page "
                    f"{result.page_number}"
                )

            context_parts.append(
                f"""
[Source {index}]
Document: {source}
Relevance Score: {result.score:.4f}

Content:
{result.content}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )