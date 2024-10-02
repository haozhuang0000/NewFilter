import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


class Llm(ChatOpenAI):
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