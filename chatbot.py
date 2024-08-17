import os

from operator import itemgetter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory

from logger import Logger
from llm import LLM
from vector_store import VectorStore
import prompt

class Chatbot():
    def __init__(self, llm_platform="openai"):
        self.logger = Logger(os.getenv("LOG_LEVEL"))

        self.vector_store = VectorStore()
        self.llm = LLM().create_llm(llm_platform)
        self.retriever = self.vector_store.get_retriever()
        self.prompt = prompt.get_prompt()
        self.memory = ConversationBufferWindowMemory(
            k=25,
            ai_prefix="Pooh and his friends",
            human_prefix="User"
        )
        self.logger.debug("[Chatbot] Chatbot system is initialised")

    def _merge_docs(self, retrieved_docs):
        self.logger.debug("[Chatbot] Merge documents")
        return "###\n\n".join([d.page_content for d in retrieved_docs])

    def _chain(self):
        self.logger.debug("[Chatbot] Create chain")
        chain_memory = RunnableParallel({
            "context": self.retriever | self._merge_docs,
            "query": RunnablePassthrough(),
            "history": RunnableLambda(self.memory.load_memory_variables) | itemgetter("history"),
            # "name": RunnablePassthrough(),
        }) | {
            "answer": self.prompt | self.llm | StrOutputParser(),
            "context": itemgetter("context"),
            "prompt": self.prompt
        }
        return chain_memory

    def _chat(self, query, user_name):
        self.logger.debug("[Chatbot] Start chat")
        chain_memory = self._chain()
        self.logger.debug("[Chatbot] Successfully generated chain")
        # result = chain_memory.invoke({"query": query, "name": user_name})
        result = chain_memory.invoke(query)
        self.logger.debug("[Chatbot] Successfully invoked chat")
        self.memory.save_context({"query": query}, {"answer": result["answer"]})
        self.logger.debug("[Chatbot] Saved the chat history")
        
        print(result["answer"])
        # print(result["prompt"].messages[0].content.split("###")[-1] + result["answer"])
        # print(result["answer"])

    def run(self):
        self.logger.debug("[Chatbot] Chatbot system is running")

        user_name = input("Could you tell us your name please?\n")

        while True:
            query = input(f"[{user_name}] ")

            if query.lower() in ["exit", "finish", "quit"]:
                print("Thank you for chatting. Goodbye!")
                break

            self._chat(query, user_name)
