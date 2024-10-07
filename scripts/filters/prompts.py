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
            You are an expert financial analyst. Based on the provided news article, determine if each of the following factors is present (1) or absent (0). Only consider the content of the article.

            Provide your answer in the following JSON format, using the exact factor descriptions as keys:

            {json_example}

            Article:
            \"\"\"
            {article}
            \"\"\"

            Factors:
            {factors}
        """
        self._prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["article", "factors", "json_example"],
            template=self._template
        )

    def get_prompt_template(self) -> PromptTemplate:
        """
        Retrieves the PromptTemplate instance.

        Returns:
            PromptTemplate: The configured prompt template.
        """
        return self._prompt_template

class CompanyRelevancePrompt:
    """
    A class to generate and manage prompts for assessing the relevance of a news article to specific companies.
    """

    def __init__(self):
        self._template: str = """
            You are an expert financial analyst. Based on the provided news article, assess how related the article is to each of the following companies. Provide a relevance score between 0 and 1 for each company, where 0 means not related at all and 1 means highly related.

            Provide your answer in the following JSON format, using the exact company names as keys:

            {json_example}

            **Please provide only the JSON output and do not include any additional text or explanations.**

            Article:
            \"\"\"
            {article}
            \"\"\"

            Companies:
            {companies}
        """
        self._prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["article", "companies", "json_example"],
            template=self._template
        )

    def get_prompt_template(self) -> PromptTemplate:
        return self._prompt_template