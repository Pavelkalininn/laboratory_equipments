import datetime
import logging
import os
from http import HTTPStatus
from json import JSONDecodeError
from typing import List, Union

import pandas
import requests
from const import (ACCESS_DENIED, ADDED, ADMIN_ADD_OR_DELETE_YOU, ADMIN_ID,
                   API_PORT, AUTHORIZATION, DELETED, EDIT, EQUIPMENT_ADD,
                   EQUIPMENT_CHANGE, EQUIPMENT_CONST, EQUIPMENT_CREATE_NAMES,
                   EQUIPMENT_SEARCH, EQUIPMENTS, EQUIPMENTS_FILTER_FIELDS,
                   EXCEL_HEADERS, FILL_IN_VALUE, FIND_FIELD, INCORRECT_COMMAND,
                   LOGIN, MAX_COUNT, NO_ONE_OBJECT_FIND, PASS_VALUES,
                   STAFF_ACCEPT, STAFF_DECLINE, SUCCESSFULLY_CREATED,
                   TOO_MANY_RESULTS, UNAUTHORIZED, USER_CREATE_NAMES,
                   USER_FORM, USER_SUCCESSFULLY_ADD_OR_DELETE, VARIANTS,
                   WEB_HOST, WITHOUT_CHANGES)
from requests import RequestException
from rest_framework.request import Request
from telebot import types


class MessageInfo:
    database = {}

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
        self.chat_information = ('', '', {})
        self.status = ''
        self.type = ''
        self.data = {}

    def is_staff_check(self):
        user_data = self.get_api_answer('', 'get', 'v1/users/me')
        if user_data.status_code == HTTPStatus.OK:
            self.is_user = True
            if user_data.json().get('is_staff'):
                self.is_staff = True

    async def authorization(self):
        if not user_status.get(self.message.chat.id):
            if not self.is_user:
                self.status = LOGIN
                new_status = (self.status, '', {})
                user_status.set(
                    self.message.chat.id, new_status
                )
                return await self.data_collect()
            if not self.is_staff:
                return await self.send_message(
                    UNAUTHORIZED,
                    self.message.chat.id
                )
        return await self.message_manager()

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
    def text_formatter(data: Union[str, list, dict]) -> list:
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

    async def status_code_parser(
            self,
            api_answer: Request
    ) -> Union[list, str]:
        try:
            if api_answer.status_code in [
                HTTPStatus.OK,
                HTTPStatus.CREATED,
            ]:
                return api_answer.json()
            if api_answer.status_code == HTTPStatus.FORBIDDEN:
                return ACCESS_DENIED
            if api_answer.status_code == HTTPStatus.BAD_REQUEST:
                if len(api_answer.json()) > 1:
                    for error in list(api_answer.json()):
                        self.data.pop(error.keys()[0])
                else:
                    self.data.pop(list(api_answer.json().keys())[0])
                return (
                    ' '.join(*api_answer.json().values())
                )
            return (
                str(api_answer.text)
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
                f'http://{WEB_HOST}:{API_PORT}/api/{endpoint}'
                f'/?{filter_expression}',
                data=data,
                headers={AUTHORIZATION: str(self.message.chat.id)},
                timeout=30
            )

        except RequestException as error:
            logging.error(error, exc_info=True)

    async def send_admin_user_apply_message(self, names, answer):
        if (
                names == USER_CREATE_NAMES
                and answer.status_code == HTTPStatus.CREATED
        ):
            await self.send_message(
                self.text_formatter(
                    await self.status_code_parser(answer)
                )[0],
                ADMIN_ID,
                [STAFF_ACCEPT, STAFF_DECLINE]
            )

    def data_field_fill_in(self, question_num, names):
        if not question_num:
            if self.type == EDIT:
                self.data['pk'] = self.get_equipment_pk_from_bot_message()
            else:
                self.data['telegram_id'] = self.message.chat.id
        else:
            for name in names:
                if name not in self.data:
                    self.data[name] = self.message.text
                    break

    async def data_collect(
            self,
    ) -> None:
        names = USER_CREATE_NAMES if self.status == LOGIN else (
            EQUIPMENT_CREATE_NAMES
        )
        user_status.set(
            self.message.chat.id,
            (self.status, self.type, self.data)
        )
        question_num = len(self.data)
        self.data_field_fill_in(question_num, names)
        buttons = (WITHOUT_CHANGES, ) if self.type == EDIT else None

        if question_num < len(names):
            for field, name in names.items():
                if field not in self.data:
                    await self.send_message(
                        FILL_IN_VALUE.format(value=name),
                        self.message.chat.id,
                        buttons
                    )
                    return
        url = "v1/users" if names == USER_CREATE_NAMES else "v1/equipments"
        method = 'post'
        if self.type == EDIT:
            url += '/' + self.data.get('pk')
            new_data = {}
            for key, value in self.data.items():
                if value not in PASS_VALUES:
                    new_data[key] = value
            self.data = new_data
            method = 'patch'

        answer = self.get_api_answer('', method, url, self.data)
        await self.send_message(
            self.text_formatter(await self.status_code_parser(answer))[0],
            self.message.chat.id,
            list(VARIANTS.keys())
        )
        await self.send_admin_user_apply_message(names, answer)
        if answer.status_code() != HTTPStatus.BAD_REQUEST:
            user_status.delete(self.message.chat.id)
        return

    def get_equipment_pk_from_bot_message(self) -> str:
        return self.message.reply_to_message.text.split(
            'id: ')[-1].split(
            '\n')[0]

    async def reply_to_message_message(self):
        if (
                self.message.chat.id == ADMIN_ID
                and SUCCESSFULLY_CREATED in self.message.reply_to_message.text
        ):
            new_user_id = self.message.reply_to_message.text.split(
                'и телеграм id '
            )[-1].split('\n')[0]
            is_staff = True if self.message.text == STAFF_ACCEPT else False
            added_or_deleted = ADDED if is_staff else DELETED
            await self.send_message(
                USER_SUCCESSFULLY_ADD_OR_DELETE.format(
                    added_or_deleted=added_or_deleted
                )
                + self.text_formatter(
                    await self.status_code_parser(
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
        if self.message.text == EQUIPMENT_CHANGE:
            self.status = EQUIPMENT_CHANGE
            self.type = EDIT
            return await self.data_collect()
        return await self.incorrect_command()

    async def message_without_status(self):
        if self.message.text == EQUIPMENT_ADD:
            self.status = EQUIPMENT_ADD
            return await self.data_collect()
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
        return await self.incorrect_command()

    async def create_and_send_excel(self, equipments):
        dataframe = pandas.DataFrame(equipments)
        now = datetime.datetime.now().strftime("%d_%m_%y_%H_%M")
        filepath = f'equipment_list_{now}.xlsx'
        dataframe.to_excel(
            filepath,
            index=False,
            sheet_name=EQUIPMENTS,
            header=EXCEL_HEADERS
        )
        with open(filepath, 'rb') as doc:
            await self.bot.send_document(self.message.chat.id, doc)
        os.remove(filepath)

    async def equipment_search(self):
        if (
                self.status == EQUIPMENT_SEARCH
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

        if self.type in EQUIPMENTS_FILTER_FIELDS.values():
            action = self.type
            equipments_without_formatter = await self.status_code_parser(
                self.get_api_answer(
                    f'{action}={self.message.text}',
                    'get',
                    'v1/equipments'
                )
            )
            equipments = self.text_formatter(
                equipments_without_formatter
            )
            if len(equipments) > MAX_COUNT:
                equipments = equipments[:MAX_COUNT]
                equipments.append(TOO_MANY_RESULTS)
            elif len(equipments) == 0:
                equipments.append(NO_ONE_OBJECT_FIND)

            for equipment in equipments:
                await self.send_message(
                    equipment,
                    self.message.chat.id,
                    list(VARIANTS.keys())
                )
            if len(equipments) > MAX_COUNT:
                await self.create_and_send_excel(equipments_without_formatter)
            self.status = ''
            return user_status.delete(self.message.chat.id)
        return await self.incorrect_command()

    async def incorrect_command(self):
        await self.send_message(
            INCORRECT_COMMAND,
            self.message.chat.id,
            list(VARIANTS.keys())
        )
        return user_status.delete(self.message.chat.id)

    async def message_manager(self) -> None:
        chat_information = user_status.get(self.message.chat.id)
        if hasattr(self.message.reply_to_message, 'text'):
            return await self.reply_to_message_message()

        if not chat_information:
            return await self.message_without_status()

        self.chat_information = chat_information
        self.status, self.type, self.data = self.chat_information
        if self.status in [LOGIN, EQUIPMENT_ADD]:
            return await self.data_collect()
        if self.status == EQUIPMENT_SEARCH:
            return await self.equipment_search()
        return await self.incorrect_command()
