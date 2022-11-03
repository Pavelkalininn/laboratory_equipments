import logging
from http import HTTPStatus
from json import JSONDecodeError
from typing import List, Union

import requests
from requests import RequestException
from rest_framework.request import Request
from settings import (ACCESS_DENIED, ADDED, ADMIN_ADD_OR_DELETE_YOU, ADMIN_ID,
                      AUTHORIZATION, DELETED, EQUIPMENT_ADD, EQUIPMENT_CONST,
                      EQUIPMENT_CREATE_NAMES, EQUIPMENT_SEARCH,
                      EQUIPMENTS_FILTER_FIELDS, FILL_IN_VALUE, FIND_FIELD,
                      INCORRECT_COMMAND, INCORRECT_STATUS, LOGIN, MAX_COUNT,
                      NO_ONE_OBJECT_FIND, STAFF_ACCEPT, STAFF_DECLINE,
                      SUCCESSFULLY_CREATED, TOO_MANY_RESULTS, UNAUTHORIZED,
                      USER_CREATE_NAMES, USER_FORM,
                      USER_SUCCESSFULLY_ADD_OR_DELETE, VARIANTS, WEB_HOST)
from telebot import types


class MessageInfo:
    database = {}

    # database = redis.Redis(
    #     host='redis',
    #     port='6379')

    def get(self, key):
        return self.database.get(key)

    def set(self, key: int, value: tuple):
        self.database[key] = value

    def delete(self, key):
        if self.database.get(key):
            self.database.pop(key)

    def keys(self):
        return list(self.database.keys())


user_status = MessageInfo()


class BotMessage:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.is_staff = False
        self.is_user = False
        self.is_staff_check()

    def is_staff_check(self):
        user_data = self.get_api_answer('', 'get', 'v1/users/me')
        if user_data.status_code == HTTPStatus.OK:
            self.is_user = True
            if user_data.json().get('is_staff'):
                self.is_staff = True

    async def authorization(self):
        if not user_status.get(self.message.chat.id):
            if not self.is_user:
                new_status = (LOGIN, '', {})
                user_status.set(
                    self.message.chat.id, new_status
                )
                return await self.data_collect(new_status)
            if not self.is_staff:
                return await self.send_message(
                    UNAUTHORIZED,
                    self.message.chat.id
                )
        return await self.text_parser()

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
            if 'inventory' in data and 'serial_number' in data:
                return [EQUIPMENT_CONST.format(**data)]
            return [data]
        for equipment in data:
            result.append(EQUIPMENT_CONST.format(**equipment))
        return result

    @staticmethod
    def status_code_parser(api_answer: Request) -> Union[list, str]:
        try:
            if api_answer.status_code in [
                HTTPStatus.OK,
                HTTPStatus.CREATED,
            ]:
                return api_answer.json()
            if api_answer.status_code == HTTPStatus.FORBIDDEN:
                return ACCESS_DENIED
            logging.error(
                INCORRECT_STATUS.format(status=api_answer.status_code),
                exc_info=True)
            return (
                str(api_answer.status_code)
                + ' '
                + api_answer.text.strip('{}')
            )
        except JSONDecodeError as error:
            logging.error(error, exc_info=True)

    def get_api_answer(
            self,
            filter_expression: str,
            method: str,
            endpoint: str,
            data: dict = None
    ) -> Request:
        try:
            return getattr(requests, method)(
                f'http://{WEB_HOST}:8000/api/{endpoint}/?{filter_expression}',
                data=data,
                headers={AUTHORIZATION: str(self.message.chat.id)},
                timeout=30
            )

        except RequestException as error:
            logging.error(error, exc_info=True)

    async def data_collect(
        self,
        chat_info: tuple,
    ) -> None:
        status, _, data = chat_info
        question_num = len(data)
        if status == LOGIN:
            names = USER_CREATE_NAMES
            user_status.set(self.message.chat.id, (LOGIN, '', data))
        else:
            names = EQUIPMENT_CREATE_NAMES
            user_status.set(self.message.chat.id, (EQUIPMENT_ADD, '', data))
        if not question_num:
            data['telegram_id'] = self.message.chat.id
        else:
            data[names[question_num - 1][0]] = self.message.text

        if question_num < len(names):
            await self.send_message(
                FILL_IN_VALUE.format(value=names[question_num][-1]),
                self.message.chat.id
            )
        else:
            if names == USER_CREATE_NAMES:
                answer = self.get_api_answer("", "post", "v1/users", data)
            else:
                answer = self.get_api_answer("", "post", "v1/equipments", data)
            await self.send_message(
                self.json_parser(self.status_code_parser(answer))[0],
                self.message.chat.id,
                list(VARIANTS.keys())
            )
            if (
                    names == USER_CREATE_NAMES
                    and answer.status_code == HTTPStatus.CREATED
            ):
                await self.send_message(
                    self.json_parser(self.status_code_parser(answer))[0],
                    ADMIN_ID,
                    [STAFF_ACCEPT, STAFF_DECLINE]
                )
            user_status.delete(self.message.chat.id)

    async def text_parser(self) -> None:
        chat_information = user_status.get(self.message.chat.id)
        if (
                self.message.chat.id == ADMIN_ID
                and hasattr(self.message.reply_to_message, 'text')
                and SUCCESSFULLY_CREATED in self.message.reply_to_message.text
        ):
            new_user_id = self.message.reply_to_message.text.split(
                'и телеграм id '
            )[-1].split(' ')[0]
            is_staff = True if self.message.text == STAFF_ACCEPT else False
            added_or_deleted = ADDED if is_staff else DELETED
            await self.send_message(
                USER_SUCCESSFULLY_ADD_OR_DELETE.format(
                    added_or_deleted=added_or_deleted
                )
                + self.json_parser(
                    self.status_code_parser(
                        self.get_api_answer(
                            '',
                            'patch',
                            'v1/users/staff_change',
                            data={'is_staff': is_staff,
                                  'new_user_id': new_user_id}
                        )
                    )
                )[0],
                self.message.chat.id
            )
            return await self.send_message(
                ADMIN_ADD_OR_DELETE_YOU.format(
                    added_or_deleted=added_or_deleted
                ),
                new_user_id,
                list(VARIANTS.keys())
            )

        if self.message.chat.id not in user_status.keys():
            if self.message.text == EQUIPMENT_ADD:
                return await self.data_collect((EQUIPMENT_ADD, '', {}))
            if self.message.text in VARIANTS:
                buttons, answer = VARIANTS.get(self.message.text)
                await self.send_message(
                    answer,
                    self.message.chat.id,
                    buttons
                )
                return user_status.set(
                    self.message.chat.id, (self.message.text, '', {})
                )

        if chat_information[0] in [LOGIN, EQUIPMENT_ADD]:
            return await self.data_collect(chat_information)

        if (
                chat_information == (EQUIPMENT_SEARCH, '', {})
                and self.message.text in EQUIPMENTS_FILTER_FIELDS
        ):
            await self.send_message(
                FIND_FIELD.format(field=self.message.text),
                self.message.chat.id
            )
            return user_status.set(
                self.message.chat.id,
                (
                    EQUIPMENT_SEARCH,
                    EQUIPMENTS_FILTER_FIELDS.get(self.message.text),
                    {}
                )
            )

        if (
                chat_information[0] == EQUIPMENT_SEARCH
                and chat_information[1]
                in EQUIPMENTS_FILTER_FIELDS.values()
        ):
            action = chat_information[1]
            equipments = self.json_parser(
                self.status_code_parser(
                    self.get_api_answer(
                        f'{action}={self.message.text}',
                        'get',
                        'v1/equipments')
                )
            )
            if len(equipments) > MAX_COUNT:
                equipments = equipments[:MAX_COUNT]
                equipments.insert(
                    0,
                    TOO_MANY_RESULTS
                )
            elif len(equipments) == 0:
                equipments.append(NO_ONE_OBJECT_FIND)

            for equipment in equipments:
                await self.send_message(
                    equipment,
                    self.message.chat.id,
                    list(VARIANTS.keys())
                )
            return user_status.delete(self.message.chat.id)

        # if chat_information == (EQUIPMENT_CHANGE, ):
        #     ...

        await self.send_message(
            INCORRECT_COMMAND + '2',
            self.message.chat.id,
            list(VARIANTS.keys())
        )
        return user_status.delete(self.message.chat.id)
