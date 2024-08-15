import os

from langchain_upstage import ChatUpstage
from llm_base import LLMBase
from logger import Logger

class UpstageWrapper(LLMBase):
    """Wrapper for Upstage Solar model"""

    def __init__(self, model_name="solar-1-mini-chat", temperature=0):
        # Initialize the Upstage Solar API client
        self.llm = ChatUpstage(
            model_name=model_name,
            temperature=temperature,
        )
        self.logger = Logger(os.getenv("LOG_LEVEL"))
        self.logger.debug("[UpstageWrapper] Upstage LLM instance is initialised")

    def get_llm(self):
        """Return the Upstage Solar LLM instance"""
        return self.llm
