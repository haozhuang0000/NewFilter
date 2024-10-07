import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


class Llm_OPENAI(ChatOpenAI):
    def __init__(self, model, openai_api_key, *args, **kwargs):
        openai_chat_models = [
            'gpt-4o',
            'gpt-4o-mini',
            'o1-preview'
        ]

        if model not in openai_chat_models:
            raise ValueError(f"Model '{model}' not supported. Available models: {openai_chat_models}")


        super().__init__(
            model_name=model,
            openai_api_key=openai_api_key,
            temperature=0,
            *args,
            **kwargs
        )

    def __call__(self, prompt):
        messages = [HumanMessage(content=prompt)]
        response = super().invoke(messages)
        return response.content

import os
from scripts.exceptions.exceptions import ModelNotFoundError
from langchain_community.llms import Ollama
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Llm(Ollama):

    def __init__(self, model, *args, **kwargs):

        ollama_host = os.getenv('OLLAMA_HOST')
        ollama_port = os.getenv('OLLAMA_PORT')

        ollama_available_models = [
            'gemma:7b',
            'gemma2:27b',
            'mistral:latest',
            'phi3:latest',
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

    def __call__(self, prompt):
        messages = [HumanMessage(content=prompt)]
        response = super().invoke(messages)
        return response