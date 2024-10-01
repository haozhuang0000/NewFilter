import os
from scripts.logger.exceptions import ModelNotFoundError
from langchain_community.llms import Ollama
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Llm(Ollama):

    def __init__(self, model, *args, **kwargs):

        ollama_host = os.getenv('OLLAMA_HOST')
        ollama_port = os.getenv('OLLAMA_PORT')

        ollama_available_models = [
            'llama3.1:8b',
            'llama3.1:70b',
            'llama3.1:70b-instruct-q4_0'
        ]

        if model not in ollama_available_models:
            raise ModelNotFoundError(model, ollama_available_models)

        super().__init__(
            model = model,
            base_url = 'http://' + str(ollama_host) + ':' + str(ollama_port),
            temperature = 0,
            *args, **kwargs
            )