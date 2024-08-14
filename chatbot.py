import os
from logger import Logger


class Chatbot():
    def __init__(self, member='all'):
        self.logger = Logger(os.getenv('LOG_LEVEL'))
        self.member = member.lower()

        if self.member == 'all':
            pass
        elif self.member == 'pooh':
            pass
        elif self.member == 'tigger':
            pass
        elif self.member == 'piglet':
            pass
        elif self.member == 'eeyore':
            pass
        else:
            pass

        self.logger.info("[Chatbot] Chatbot system initiated")

    def run(self):
        self.logger.info("[Chatbot] Chatbot system is running.")
