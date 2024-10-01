from langchain.prompts import PromptTemplate


class NewsFilterExpertPrompt:
    """
    A class to generate and manage prompts for a world-renowned financial expert assistant.

    This class utilizes LangChain's PromptTemplate to format prompts with the provided
    context and user input. It ensures that responses adhere to the specified guidelines,
    including handling cases where the knowledge base does not contain relevant information.
    """

    def __init__(self):
        """
        Initializes the NewsFilterExpertPrompt with a predefined template.
        """
        self._template: str = """
            {context}

            The ONLY Question for you to answer: {input}
        """
        self._prompt_template: PromptTemplate = PromptTemplate.from_template(self._template)

    def get_prompt_template(self) -> PromptTemplate:
        """
        Retrieves the PromptTemplate instance.

        Returns:
            PromptTemplate: The configured prompt template.
        """
        return self._prompt_template