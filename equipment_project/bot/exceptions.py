import logging


class BotException(Exception):

    def __init__(self, message):
        logging.error(message)
