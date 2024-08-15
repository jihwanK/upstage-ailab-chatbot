import os

from langchain_openai import ChatOpenAI

from llm_base import LLMBase
from logger import Logger

class OpenAIWrapper(LLMBase):
    """Wrapper for OpenAI's GPT models"""

    def __init__(self, model_name="gpt-3.5-turbo", temperature=0):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        self.logger = Logger(os.getenv("LOG_LEVEL"))
        self.logger.debug("[OpenAIWrapper] OpenAI LLM instance is initialised")

    def get_llm(self):
        """Return the OpenAI LLM instance"""
        return self.llm
