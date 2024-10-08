import json
from typing import Dict, List
from prompts import NewsFilterExpertPrompt, CompanyRelevancePrompt
from llm import Llm

class NewsFilter:
    def __init__(self, llm: Llm, categories: Dict[str, List[str]]):
        """
        Initializes the NewsFilter with an LLM instance and categories.

        Args:
            llm (Llm): An instance of the Llm class for making API calls.
            categories (Dict[str, List[str]]): A dictionary of categories and their factors.
        """
        self.llm = llm
        self.categories = categories
        self.news_filter_prompt_template = NewsFilterExpertPrompt().get_prompt_template()
        self.company_relevance_prompt_template = CompanyRelevancePrompt().get_prompt_template()

    def get_filter(self, article_text: str) -> Dict[str, Dict[str, int]]:
        """
        Analyzes the article and returns the presence of factors under each category.

        Args:
            article_text (str): The news article text to analyze.

        Returns:
            Dict[str, Dict[str, int]]: A dictionary with categories as keys and factor presence as values.
        """
        results = {}

        for large_category, factors in self.categories.items():
            print(f"Analyzing category: {large_category}")

            # Format the factors list
            factors_list = '\n'.join(f"- {factor}" for factor in factors)

            # Generate the JSON example with the actual factors
            json_example = {
                "results": {
                    factor: "0 or 1" for factor in factors
                }
            }
            json_example_str = json.dumps(json_example, indent=4)

            # Generate the prompt using the prompt template
            prompt = self.news_filter_prompt_template.format(
                article=article_text.strip(),
                factors=factors_list.strip(),
                json_example=json_example_str
            )

            # Make the LLM call
            response = self.llm(prompt)

            # Parse the response
            try:
                # Extract the JSON part from the response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1  # Find the last '}'
                json_str = response[json_start:json_end]

                # Remove any backticks and extra whitespace
                json_str = json_str.strip().strip('`')

                # Parse the JSON string
                response_json = json.loads(json_str)

                # Add the results to the main dictionary
                factors_results = response_json.get('results', {})
                # Convert string scores to integers
                factors_results = {factor: int(score) for factor, score in factors_results.items()}
                results[large_category] = factors_results
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing JSON response for category '{large_category}': {e}")
                # Assign None or handle accordingly
                results[large_category] = {factor: None for factor in factors}

        return results
    def get_company_relevance(self, article_text: str, company_names: List[str]) -> Dict[str, float]:
        """
        Analyzes the article and returns relevance scores for each company.

        Args:
            article_text (str): The news article text to analyze.
            company_names (List[str]): A list of company names.

        Returns:
            Dict[str, float]: A dictionary with company names as keys and relevance scores as values.
        """
        if not company_names:
            # If no company names are provided, return an empty dictionary
            return {}

        # Prepare the list of companies
        companies_list = '\n'.join(f"- {company_name}" for company_name in company_names)

        # Generate the JSON example with the actual company names
        json_example = {
            "relevance_scores": {
                company_name: "score between 0 and 2" for company_name in company_names
            }
        }
        json_example_str = json.dumps(json_example, indent=4)

        # Generate the prompt using the prompt template
        prompt = self.company_relevance_prompt_template.format(
            article=article_text.strip(),
            companies=companies_list.strip(),
            json_example=json_example_str
        )

        # Make the LLM call
        response = self.llm(prompt)

        # Parse the response
        try:
            # Extract the JSON part from the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1  # Find the last '}'
            json_str = response[json_start:json_end]

            # Remove any backticks and extra whitespace
            json_str = json_str.strip().strip('`')

            # Parse the JSON string
            response_json = json.loads(json_str)

            # Get the relevance scores
            relevance_scores = response_json.get('relevance_scores', {})

            # Convert string scores to floats
            relevance_scores = {company_name: float(score) for company_name, score in relevance_scores.items()}

            return relevance_scores
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing JSON response for company relevance: {e}")
            # Assign None or handle accordingly
            return {company_name: None for company_name in company_names}