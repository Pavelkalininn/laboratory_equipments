import logging


class BotError(Exception):

    def __init__(self, message):
        logging.error(message)
