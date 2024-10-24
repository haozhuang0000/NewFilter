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
            You are an expert financial analyst. Based on the provided news article, assess how related the article is to each of the following companies. Provide a relevance score between 0 and 2 for each company, where:

            - **0**: The company isn't mentioned at all in the news.
            - **1**: The company is mentioned but isn't the main focus.
            - **2**: The company is most mentioned or is the main focus of the news.

            **Important**: Carefully determine if the news is talking about the specific company listed or a different company with a similar name. Pay close attention to company identifiers such as "Inc.", "Ltd.", or country-specific designations to avoid confusion (e.g., "Tesla Inc" vs. "Tesla a.s.").

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


class CompanyImportance:
    """
    A class to generate and manage prompts for assessing the relevance of a news article to specific companies.
    """

    def __init__(self):
        self._template: str = """
            You are an expert financial analyst. You will be provided with a dictionary, base on your own understanding and knowledge of this company, you will need to give a importance score (1 to 10) for each factories for this company.
            
            Dictionaries:
            \"\"\"
            {factors}
            \"\"\"
            
            Company:
            {companies}
            
            Provide your answer in the following JSON format, using the exact company names as keys:
            {json_example}
            
            You need to think and provide answer base on following steps, you can think longer:

            1. Understand this company first
            2. Provide score for each factor base on your understanding and knowledge
            3. You do not need to put your understanind into the json output, only output the factors
        """
        self._prompt_template: PromptTemplate = PromptTemplate(
            input_variables=["factors", "companies", "json_example"],
            template=self._template
        )

    def get_prompt_template(self) -> PromptTemplate:
        return self._prompt_template