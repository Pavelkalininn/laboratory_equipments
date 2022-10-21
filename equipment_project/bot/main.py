import asyncio
import logging
import os
import sys
from http import HTTPStatus
from json import JSONDecodeError
from typing import Union, List

import requests
from dotenv import load_dotenv
from exceptions import BotError
from requests import RequestException
from telebot import ExceptionHandler, types
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEB_HOST = os.getenv('WEB_HOST')
MAX_COUNT = 10
EQUIPMENT_ADD = 'Добавить оборудование'
EQUIPMENT_SEARCH = 'Поиск оборудования'
EQUIPMENT_CHANGE = 'Изменить информацию о оборудовании'
VARIANTS = {
    EQUIPMENT_SEARCH:
        [
            ['Наименование',
             'Инвентарный номер',
             'Модель',
             'Серийный номер',
             'Код ТН ВЭД ЕАЭС',
             'Местонахождение'
             ],
            'По какому полю будем вести поиск?'
        ],
    EQUIPMENT_CHANGE:
        [[], 'Введите инвентарный номер / наименование оборудования'],
    EQUIPMENT_ADD:
        [[], 'Введите инвентарный номер']

}
INCORRECT_COMMAND = (
    'Введенная команда не используется, необходимо выбрать команду из '
    'предложенных вариантов'
)

FIRST, SECOND, THIRD, FOURTH = range(4)
INFO = 'Бот для просмотра и внесения сведений по оборудованию'
BUTTON_START = ['/start']
ANY_THINK_WAS_WRONG = (
    'Что-то пошло не так, если ошибка повторится - обратитесь к администратору'
)
EQUIPMENTS_FILTER_FIELDS = {
    'Наименование': 'name',
    'Инвентарный номер': 'inventory',
    'Модель': 'model',
    'Серийный номер': 'serial_number',
    'Код ТН ВЭД ЕАЭС': 'nomenclature_key',
    'Местонахождение': 'movement'
}
user_status = {}
EQUIPMENT_CONST = (
    '''id: {id}
Инвентарный номер: {inventory}

Наименование: {name}
Серийный номер: {serial_number}
Модель: {model}
Изготовитель: {manufacturer}
Код ТН ВЭД: {nomenclature_key}
Документы: {documents}
Путь к папке с документами: {document_path}

Аренда: {rents}
Аттестаты: {attestations}

Калибровки: {calibrations}
Местоположения: {movements}
Последнее изменение пользователем: {creator}
'''
)

EQUIPMENT_CREATE_NAMES = [
    ('inventory', 'инвентарный номер'),
    ('name', 'наименование'),
    ('serial_number', 'серийный номер'),
    ('model', 'модель'),
    ('manufacturer', 'изготовителя'),
    ('nomenclature_key', 'Код ТН ВЭД'),
    ('document_path', 'Путь к папке с документацией')
]


class BotExceptionHandler(ExceptionHandler):
    def handle(self, exception):
        logging.error(exception)


def check_tokens():
    """Проверка наличия переменных окружения."""
    return TELEGRAM_TOKEN and WEB_HOST


async def send_message(bot, chat_id: int, message: str,
                       buttons: List[str] = None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if buttons:
        keyboard.add(*buttons)
    await bot.send_message(
        chat_id,
        message,
        reply_markup=keyboard
    )


def equipment_parser(data: Union[str, list, dict]) -> list:
    result = []
    if isinstance(data, str):
        return [data]
    elif isinstance(data, dict):
        result = [data]
    else:
        for equipment in data:
            logging.info(equipment)
            result.append(EQUIPMENT_CONST.format(**equipment))
    return result


def get_api_answer(
        sender_id: int,
        message: str,
        method: str,
        endpoint: str,
        data: dict = None
) -> Union[list, str]:
    try:
        api_answer = getattr(requests, method)(
            f'http://{WEB_HOST}/api/v1/{sender_id}/{endpoint}/?{message}',
            data=data,
            timeout=30
        )
        if api_answer.status_code not in [
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        ]:
            logging.error('Некорректный статус от API', exc_info=True)
            return ANY_THINK_WAS_WRONG + ' Код: ' + str(api_answer.status_code)
        return api_answer.json()
    except RequestException as error:
        logging.error(error, exc_info=True)
    except JSONDecodeError as error:
        logging.error(error, exc_info=True)


async def equipment_data_collect(bot, chat_id, chat_info, text) -> None:
    data = chat_info[-1]
    question_num = len(data)
    data[EQUIPMENT_CREATE_NAMES[question_num][0]] = text
    user_status[chat_id] = (EQUIPMENT_ADD, '', data)

    if question_num < len(EQUIPMENT_CREATE_NAMES) - 1:
        await send_message(
            bot,
            chat_id,
            f'Введите {EQUIPMENT_CREATE_NAMES[question_num + 1][-1]}'
        )
    else:
        await send_message(
            bot,
            chat_id,
            equipment_parser(
                get_api_answer(chat_id, "", "post", "equipments", data)
            )[0]
        )
        user_status.pop(chat_id)


async def text_parser(bot, chat_id, text):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*VARIANTS.keys())
    chat_information = user_status.get(chat_id)
    if chat_id not in user_status and text in VARIANTS:
        buttons, answer = VARIANTS.get(text)
        await send_message(
            bot,
            chat_id,
            answer,
            buttons
        )
        logging.info('Status first')
        user_status[chat_id] = (text, '', {})

    elif (
            chat_information == (EQUIPMENT_SEARCH, '', {})
            and text in EQUIPMENTS_FILTER_FIELDS
    ):
        await send_message(
            bot,
            chat_id,
            f'Ищем по полю {text}, введите значение',

        )
        user_status[chat_id] = (
            EQUIPMENT_SEARCH,
            EQUIPMENTS_FILTER_FIELDS.get(text),
            {}
        )

    elif (
            chat_information[0] == EQUIPMENT_SEARCH
            and chat_information[1]
            in EQUIPMENTS_FILTER_FIELDS.values()
    ):
        print('filter')
        action = chat_information[1]
        equipments = equipment_parser(
            get_api_answer(
                chat_id,
                f'{action}={text}',
                'get',
                'equipments')
        )
        if len(equipments) > MAX_COUNT:
            equipments = equipments[:MAX_COUNT]
            equipments.insert(
                0,
                'Слишком много результатов, будут показаны первые '
                f'{MAX_COUNT}, '
                'попробуйте усложнить критерии поиска или работать с '
                'web версией!'
            )
        elif len(equipments) == 0:
            equipments.append('Не найдено ни одного подходящего объекта')

        for equipment in equipments:
            await bot.send_message(
                chat_id,
                equipment,
                reply_markup=keyboard
            )
        user_status.pop(chat_id)

    # elif chat_information == (EQUIPMENT_CHANGE, ):
    #     ...
    elif EQUIPMENT_ADD in chat_information:
        print('add')
        await equipment_data_collect(bot, chat_id, chat_information, text)

    else:
        print('else')
        await bot.send_message(
            chat_id,
            INCORRECT_COMMAND,
            reply_markup=keyboard
        )
        logging.info('incorrect')
        user_status[chat_id] = (FIRST, '', {})


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
    bot = AsyncTeleBot(TELEGRAM_TOKEN, exception_handler=ExceptionHandler())

    @bot.message_handler(commands=['start'])
    async def start(message: Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*VARIANTS.keys())
        await bot.send_message(message.chat.id, INFO, reply_markup=keyboard)
        user_status.pop(message.chat.id)

    @bot.message_handler(content_types=['text'])
    async def input_text(message: Message):
        await text_parser(bot, message.chat.id, message.text)

    asyncio.run(
        bot.polling(none_stop=True, timeout=60, request_timeout=600)
    )


if __name__ == '__main__':
    main()
