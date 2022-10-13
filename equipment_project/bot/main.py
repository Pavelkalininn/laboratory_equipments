import asyncio
import logging
import os
import sys
from http import HTTPStatus
from json import JSONDecodeError

import requests
from dotenv import load_dotenv
from exceptions import BotError
from requests import RequestException
from telebot import ExceptionHandler, types
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEB_HOST = os.getenv("WEB_HOST")

VARIANTS = {
    'Отобразить текущюю привязку оборудования по инвентарному/наименованию':
        [[], 'Введите инвентарный номер / наименование оборудования'],
    'Изменить информацию о оборудовании':
        [[], 'Введите инвентарный номер / наименование оборудования'],
    'Поиск оборудования':
        [
            ['Наименованине', 'Код ТН ВЭД ЕАЭС'],
            'Выберите по какой графе искать'
        ],
    'Списки оборудования по площадкам':
        [[], 'Выберите площадку'],
    'Добавить оборудование':
        [[], 'Введите инвентарный номер']

}
INCORRECT_COMMAND = (
    'Введенная команда не используется, необходимо выбрать команду из '
    'предложенных вариантов'
)
FIRST, SECOND, THIRD, FOURTH = range(4)
INFO = 'Бот для просмотра и внесения сведений по оборудованию'
BUTTON_START = ['/start']
user_status = {}
TRAINEE = {
    "inventory": 16,
    "name": "Name",
    "serial_number": "21",
    "model": "45r",
    "manufacturer": "Manufacturer",
    "nomenclature_key": 8800555333,
    "documents": [
        1,
        2
    ],
    "document_path": "C:/",
    "telegram_id": "1",
    "rents": [
        1
    ],
    "attestations": [
        1
    ]
}


class BotExceptionHandler(ExceptionHandler):
    def handle(self, exception):
        logging.error(exception)


def check_tokens():
    """Проверка наличия переменных окружения."""
    return TELEGRAM_TOKEN and WEB_HOST


async def text_parser(bot, chat_id, text):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if chat_id not in user_status:
        if text in VARIANTS:
            buttons, answer = VARIANTS.get(text)
            keyboard.add(*buttons)
            await bot.send_message(
                chat_id,
                answer,
                reply_markup=keyboard
            )
            user_status[chat_id] = FIRST
        else:
            await bot.send_message(
                chat_id,
                INCORRECT_COMMAND,
                reply_markup=keyboard
            )
    else:
        if user_status.get(chat_id) == FIRST:
            await bot.send_message(
                chat_id,
                get_api_answer(chat_id, text, 'get', 'equipments'),
                reply_markup=keyboard
            )


def get_api_answer(sender_id, message, method, endpoint):
    """Возвращает ответ от API."""
    try:
        api_answer = getattr(requests, method)(
            f'http://{WEB_HOST}:8000/api/v1/{endpoint}/',
            data=TRAINEE,
            timeout=30
        )
        if api_answer.status_code != HTTPStatus.OK:
            return f'{api_answer} -- {api_answer.status_code} --'
        return api_answer.json()
    except RequestException as error:
        logging.error(error, exc_info=True)
    except JSONDecodeError as error:
        logging.error(error, exc_info=True)


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout), ],
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s')
    bot = AsyncTeleBot(TELEGRAM_TOKEN, exception_handler=ExceptionHandler())
    logging.info('Запуск бота')

    if not check_tokens():
        logging.critical('Отсутствуют переменные окружения.')
        raise BotError('Программа принудительно остановлена.'
                           ' Отсутствуют переменные окружения.')

    @bot.message_handler(commands=['start'])
    async def start(message: Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*VARIANTS.keys())
        await bot.send_message(message.chat.id, INFO, reply_markup=keyboard)
        user_status.pop(message.chat.id)

    @bot.message_handler(content_types=['text'])
    async def input_text(message: Message):
        await text_parser(bot, message.chat.id, message.text)

    asyncio.run(bot.polling(none_stop=True, timeout=60, request_timeout=600))


if __name__ == '__main__':
    main()
