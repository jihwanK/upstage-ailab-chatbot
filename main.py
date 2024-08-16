import os
from dotenv import load_dotenv
load_dotenv(override=True)

from logger import Logger
from chatbot import Chatbot

def main():
    logger = Logger(os.getenv("LOG_LEVEL"))
    logger.debug("[main] Start")

    # chatbot = Chatbot(logger, "pooh")
    chatbot = Chatbot(llm_platform="openai")
    chatbot.run()


if __name__ == "__main__":
    main()
