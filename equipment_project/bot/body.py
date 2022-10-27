import logging
from http import HTTPStatus
from json import JSONDecodeError
from typing import Union, List

import requests
from requests import RequestException
from telebot import types

from bot.settings import (USER_FORM, EQUIPMENT_CONST, WEB_HOST,
                          ANY_THINK_WAS_WRONG, LOGIN, USER_CREATE_NAMES,
                          EQUIPMENT_CREATE_NAMES,
                          EQUIPMENT_ADD, VARIANTS, ADMIN_ID, STAFF_ACCEPT,
                          INCORRECT_COMMAND,
                          EQUIPMENT_SEARCH, EQUIPMENTS_FILTER_FIELDS,
                          MAX_COUNT, STAFF_DECLINE)

user_status = {}


class BotMessage:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def send_message(
            self,
            message: str,
            chat_id: int,
            buttons: List[str] = None
    ):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if buttons:
            keyboard.add(*buttons)
        await self.bot.send_message(
            chat_id,
            message,
            reply_markup=keyboard
        )

    @staticmethod
    def json_parser(data: Union[str, list, dict]) -> list:
        result = []
        if isinstance(data, str) or isinstance(data, dict):
            if 'email' in data and 'first_name' in data:
                return [USER_FORM.format(**data)]
            return [data]
        else:
            for equipment in data:
                logging.info(equipment)
                result.append(EQUIPMENT_CONST.format(**equipment))
        return result

    def user_create(
            self,
            data: dict = None
    ) -> Union[list, str]:
        try:
            data['telegram_id'] = self.message.chat.id
            api_answer = requests.post(
                f'http://{WEB_HOST}/api/users/',
                data=data,
                timeout=30
            )
            if api_answer.status_code not in [
                HTTPStatus.CREATED,
            ]:
                logging.error('Некорректный статус от API', exc_info=True)
                return (
                        ANY_THINK_WAS_WRONG
                        + ' Код: /n '
                        + str(api_answer.status_code)
                        + " "
                        + str(api_answer.json().values())
                )
            return api_answer.json()
        except RequestException as error:
            logging.error(error, exc_info=True)
        except JSONDecodeError as error:
            logging.error(error, exc_info=True)

    def get_api_answer(
            self,
            message: str,
            method: str,
            endpoint: str,
            data: dict = None
    ) -> Union[list, str]:
        data['telegram_id'] = self.message.chat.id
        try:
            api_answer = getattr(requests, method)(
                f'http://{WEB_HOST}/api/v1/{endpoint}/?{message}',
                data=data,
                timeout=30
            )
            if api_answer.status_code not in [
                HTTPStatus.OK,
                HTTPStatus.CREATED,
            ]:
                logging.error('Некорректный статус от API', exc_info=True)
                return (
                        ANY_THINK_WAS_WRONG
                        + ' Код: /n '
                        + str(api_answer.status_code)
                        + " "
                        + str(api_answer.json().values())
                )
            return api_answer.json()
        except RequestException as error:
            logging.error(error, exc_info=True)
        except JSONDecodeError as error:
            logging.error(error, exc_info=True)

    async def data_collect(
            self,
            chat_info,
    ) -> None:
        status, _, data = chat_info
        question_num = len(data)
        if status == LOGIN:
            names = USER_CREATE_NAMES
            user_status[self.message.chat.id] = (LOGIN, '', data)
        else:
            names = EQUIPMENT_CREATE_NAMES
            user_status[self.message.chat.id] = (EQUIPMENT_ADD, '', data)
        data[names[question_num][0]] = self.message.text

        if question_num < len(names) - 1:
            await self.send_message(
                f'Введите {names[question_num + 1][-1]}',
                self.message.chat.id
            )
        else:
            if names == USER_CREATE_NAMES:
                answer = self.user_create(data)
            else:
                answer = self.get_api_answer("", "post", "equipments", data)
            await self.send_message(
                self.json_parser(answer)[0],
                self.message.chat.id,
                list(VARIANTS.keys())
            )
            if names == USER_CREATE_NAMES:
                await self.send_message(
                    self.json_parser(answer)[0],
                    ADMIN_ID,
                    [STAFF_ACCEPT, STAFF_DECLINE]
                )
            user_status.pop(self.message.chat.id)

    async def text_parser(self):
        chat_information = user_status.get(self.message.chat.id)

        if (
                self.message.chat.id == ADMIN_ID
                and hasattr(self.message.reply_to_message, 'text')
                and 'Успешно создан!' in self.message.reply_to_message.text
        ):
            new_user_id = self.message.reply_to_message.text.split(
                'и телеграм id '
            )[-1].split(' ')[0]
            is_staff = True if self.message.text == STAFF_ACCEPT else False
            await self.send_message(
                f'Пользователь успешно добавлен' + self.json_parser(
                    self.get_api_answer(
                        '',
                        'patch',
                        'staff/staff_change',
                        data={'is_staff': is_staff, 'new_user_id': new_user_id}
                    )
                )[0],
                self.message.chat.id

            )

        elif self.message.chat.id not in user_status:
            if self.message.text in VARIANTS:
                buttons, answer = VARIANTS.get(self.message.text)
                await self.send_message(
                    answer,
                    self.message.chat.id,
                    buttons
                )
                logging.info('Status first')
                user_status[self.message.chat.id] = (self.message.text, '', {})
            else:
                await self.send_message(

                    INCORRECT_COMMAND + '1',
                    self.message.chat.id,
                    list(VARIANTS.keys())
                )
                logging.info('incorrect')
                user_status.pop(self.message.chat.id)

        elif chat_information[0] == LOGIN:
            await self.data_collect(chat_information)
        elif (
                chat_information == (EQUIPMENT_SEARCH, '', {})
                and self.message.text in EQUIPMENTS_FILTER_FIELDS
        ):
            await self.send_message(
                f'Ищем по полю {self.message.text}, введите значение',
                self.message.chat.id

            )
            user_status[self.message.chat.id] = (
                EQUIPMENT_SEARCH,
                EQUIPMENTS_FILTER_FIELDS.get(self.message.text),
                {}
            )

        elif (
                chat_information[0] == EQUIPMENT_SEARCH
                and chat_information[1]
                in EQUIPMENTS_FILTER_FIELDS.values()
        ):
            action = chat_information[1]
            equipments = self.json_parser(
                self.get_api_answer(
                    f'{action}={self.message.text}',
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
                await self.send_message(
                    equipment,
                    self.message.chat.id,
                    list(VARIANTS.keys())
                )
            user_status.pop(self.message.chat.id)

        # elif chat_information == (EQUIPMENT_CHANGE, ):
        #     ...
        elif EQUIPMENT_ADD in chat_information:
            await self.data_collect(chat_information)
        else:
            await self.send_message(
                INCORRECT_COMMAND + '2',
                self.message.chat.id,
                list(VARIANTS.keys())
            )
            logging.info('incorrect')
            user_status.pop(self.message.chat.id)
