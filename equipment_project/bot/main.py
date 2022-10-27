import asyncio
import logging
import sys

from body import user_status, BotMessage
from settings import ADMIN_ID, WEB_HOST, TELEGRAM_TOKEN, LOGIN, INFO
from exceptions import BotError
from telebot import ExceptionHandler
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


def check_tokens():
    """Проверка наличия переменных окружения."""
    return TELEGRAM_TOKEN and WEB_HOST and ADMIN_ID


def main():
    """Bot`s main logic."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), ],
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s')
    logging.info('Запуск бота')

    if not check_tokens():
        logging.critical('Отсутствуют переменные окружения.')
        raise BotError(
            'Программа принудительно остановлена.'
            ' Отсутствуют переменные окружения.'
        )
    bot = AsyncTeleBot(
        TELEGRAM_TOKEN,
        exception_handler=ExceptionHandler()
    )

    async def text_parser(message: Message):
        message = BotMessage(bot, message)
        await message.text_parser()

    @bot.message_handler(commands=['start'])
    async def start(message: Message):
        await text_parser(message)

    @bot.message_handler(commands=['help', 'h'])
    async def help_text(message: Message):
        await bot.send_message(message.chat.id, INFO)

    @bot.message_handler(content_types=['text'])
    async def input_text(message: Message):
        await text_parser(message)

    asyncio.run(
        bot.polling(none_stop=True, timeout=60, request_timeout=600)
    )


if __name__ == '__main__':
    main()
