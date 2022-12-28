import asyncio
import logging
import sys

from body import (
    BotMessage,
)
from const import (
    ADMIN_ID,
    INFO,
    TELEGRAM_TOKEN,
    WEB_HOST,
)
from exceptions import (
    BotError,
)
from telebot import (
    ExceptionHandler,
    apihelper,
)
from telebot.async_telebot import (
    AsyncTeleBot,
)
from telebot.types import (
    Message,
)


class DebugExceptionHandler(ExceptionHandler):
    """
    Class for handling and raise exceptions while Polling in debug developer
     mode
    """
    def handle(self, exception):
        raise exception


def check_tokens():
    """Environment constants check."""
    return TELEGRAM_TOKEN and WEB_HOST and ADMIN_ID


def main(bot_token: str = None, bot_url: str = None):
    """Bot`s main logic."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), ],
        format=(
            '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %('
            'message)s '
        )
    )
    logging.info('Запуск бота')
    if bot_url:
        apihelper.API_URL = bot_url

    if not check_tokens():
        logging.critical('Отсутствуют переменные окружения.')
        raise BotError(
            'Программа принудительно остановлена.'
            ' Отсутствуют переменные окружения.'
        )

    bot = AsyncTeleBot(
        bot_token or TELEGRAM_TOKEN,
        exception_handler=(
            DebugExceptionHandler()
            if WEB_HOST == 'localhost'
            else ExceptionHandler()
        )
    )

    async def text_manager(message: Message):
        message = BotMessage(bot, message)
        await message.authorization()

    @bot.message_handler(commands=['start'])
    async def start(message: Message):
        await text_manager(message)

    @bot.message_handler(commands=['help', 'h'])
    async def help_text(message: Message):
        await bot.send_message(message.chat.id, INFO)

    @bot.message_handler(content_types=['text'])
    async def input_text(message: Message):
        await text_manager(message)

    return asyncio.run(
        bot.polling(none_stop=True, timeout=60, request_timeout=600)
    )


if __name__ == '__main__':
    main()
