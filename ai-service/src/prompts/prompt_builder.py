from src.prompts.prompt_templates import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)


class PromptBuilder:
    """
    Builds the final prompts sent to the LLM.
    """

    def build(
        self,
        question: str,
        context: str,
    ) -> dict:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not context.strip():
            raise ValueError(
                "Context cannot be empty."
            )

        user_prompt = (
            USER_PROMPT_TEMPLATE.format(
                context=context,
                question=question,
            )
        )

        return {
            "system": SYSTEM_PROMPT.strip(),
            "user": user_prompt.strip(),
        }