import datetime
import logging
import os
from http import (
    HTTPStatus,
)
from json import (
    JSONDecodeError,
)
from typing import (
    List,
    Union,
)

import requests
from const import (
    ACCESS_DENIED,
    ADDED,
    ADMIN_ADD_OR_DELETE_YOU,
    ADMIN_ID,
    API_PORT,
    AUTHORIZATION,
    DATE_FORM,
    DELETED,
    EQUIPMENT_ACTION_BUTTONS,
    EQUIPMENT_CONST,
    EQUIPMENT_SEARCH,
    EQUIPMENTS,
    EQUIPMENTS_FILTER_FIELDS,
    EXCEL_HEADERS,
    FILENAME,
    FILL_IN_VALUE,
    FIND_FIELD,
    INCORRECT_COMMAND,
    LOGIN,
    MAX_COUNT,
    MOVEMENT_ADD,
    MOVEMENT_CREATE_NAMES,
    NO_ONE_OBJECT_FIND,
    QUIT,
    STAFF_ACCEPT,
    STAFF_DECLINE,
    STATUS,
    STATUS_REMOVE,
    STATUS_TYPE,
    SUCCESSFULLY_CREATED,
    TODAY,
    TOO_MANY_RESULTS,
    UNAUTHORIZED,
    USER_CREATE_NAMES,
    USER_FORM,
    USER_SUCCESSFULLY_ADD_OR_DELETE,
    WEB_HOST,
)
from pandas import (
    DataFrame,
)
from redis_storage import (
    MessageInfo,
)
from requests import (
    RequestException,
)
from rest_framework.request import (
    Request,
)
from telebot import (
    types,
)
from telebot.async_telebot import (
    AsyncTeleBot,
)

user_status = MessageInfo()


class BotMessage:
    def __init__(self, bot: AsyncTeleBot, message: types.Message) -> None:
        self.bot = bot
        self.message = message
        self.id = self.message.chat.id
        self.is_staff = False
        self.is_user = False
        self.is_staff_check()

    def is_staff_check(self) -> None:
        user_data = self.get_api_answer('', 'get', 'v1/users/me')
        if user_data and user_data.status_code in (HTTPStatus.OK,):
            self.is_user = True
            if user_data.json().get('is_staff'):
                self.is_staff = True

    async def authorization(self) -> None:
        if not user_status.exists(self.message.chat.id):
            if not self.is_user:
                user_status.set_status(self.message.chat.id, LOGIN)
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
    ) -> None:
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
            if 'inventory' in data and 'manual' in data:
                return [EQUIPMENT_CONST.format(**data)]
            return [data]
        if isinstance(data, list):
            for value in data:
                if 'address' in value:
                    result.append(value.get('address'))
                else:
                    result.append(EQUIPMENT_CONST.format(**value))
        return result

    async def status_code_parser(
            self,
            api_answer: Request
    ) -> Union[list, str]:
        try:
            if api_answer.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.CREATED,
            ):
                return api_answer.json()
            if api_answer.status_code in (HTTPStatus.FORBIDDEN,):
                return ACCESS_DENIED
            if api_answer.status_code in (HTTPStatus.BAD_REQUEST,):
                if len(api_answer.json()) > 1:
                    user_status.remove_data_value(
                        self.id,
                        list(api_answer.json().keys())
                    )
                else:
                    bad_object = list(api_answer.json().keys())
                    user_status.remove_data_value(
                        self.id,
                        bad_object
                    )
                return (
                    ' '.join(
                        f'{key} {" ".join(value)}'
                        for key, value in api_answer.json().items())
                )
            return (
                str(api_answer.text)
            )
        except JSONDecodeError as error:
            logging.error(error, exc_info=True)
        except KeyError as error:
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
                headers={AUTHORIZATION: str(self.id)},
                timeout=30
            )

        except RequestException as error:
            logging.error(error, exc_info=True)

    async def send_admin_user_apply_message(
            self,
            names: dict,
            answer: Request
    ):
        if (
                names in (USER_CREATE_NAMES,)
                and answer.status_code in (HTTPStatus.CREATED,)
        ):
            await self.send_message(
                self.text_formatter(
                    await self.status_code_parser(answer)
                )[0],
                ADMIN_ID,
                [STAFF_ACCEPT, STAFF_DECLINE]
            )

    def data_field_fill_in(self, question_num: int, names: dict) -> None:
        if not question_num:
            if user_status.get_status(self.id) in (MOVEMENT_ADD,):
                user_status.set_item(
                    self.id,
                    'equipment',
                    self.get_equipment_pk_from_bot_message()
                )
            else:
                user_status.set_item(
                    self.id,
                    'telegram_id',
                    str(self.id)
                )
        else:
            for name in names:
                if not user_status.get_data_value(
                        self.id,
                        name
                ):
                    user_status.set_item(
                        self.id,
                        name,
                        self.message.text
                    )
                    break

    async def data_collect(self) -> None:
        names = USER_CREATE_NAMES if user_status.get_status(
            self.id
        ) in (LOGIN,) else (
            MOVEMENT_CREATE_NAMES
        )

        question_num = len(user_status.get_data(self.id))
        self.data_field_fill_in(question_num, names)
        buttons = [QUIT, ]
        data = user_status.get_data(self.id)
        if user_status.get_status(self.id) in (MOVEMENT_ADD,):
            if len(data) == 1:
                buttons.append(TODAY)
            if len(data) > 2:
                answer = self.text_formatter(
                    await self.status_code_parser(
                        self.get_api_answer(
                            '', 'get', 'v1/destinations', {}
                        )
                    )
                )
                buttons += answer

        if question_num < len(names):
            for field, name in names.items():
                if not user_status.get_data_value(self.id, field):
                    await self.send_message(
                        FILL_IN_VALUE.format(value=name),
                        self.id,
                        buttons
                    )
                    return
        url = "v1/users" if names in (USER_CREATE_NAMES,) else "v1/movements"
        method = 'post'
        answer = self.get_api_answer(
            '', method, url, user_status.get_data(self.id)
        )
        await self.send_message(
            self.text_formatter(
                await self.status_code_parser(answer)
            )[0],
            self.id,
            EQUIPMENT_ACTION_BUTTONS
        )
        await self.send_admin_user_apply_message(names, answer)
        if answer.status_code != HTTPStatus.BAD_REQUEST:
            user_status.delete(self.message.chat.id)
        return

    def get_equipment_pk_from_bot_message(self) -> str:
        return self.message.reply_to_message.text.split(
            'id: ')[-1].split(
            '\n')[0]

    async def reply_to_message_message(self) -> None:
        if (
                self.message.chat.id in (ADMIN_ID,)
                and SUCCESSFULLY_CREATED in self.message.reply_to_message.text
        ):
            new_user_id = int(self.message.reply_to_message.text.split(
                'и телеграм id '
            )[-1].split('\n')[0])
            is_staff = True if self.message.text in (STAFF_ACCEPT,) else False
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
                EQUIPMENT_ACTION_BUTTONS
            )

        if self.message.text in (MOVEMENT_ADD,):
            user_status.set_status(self.id, self.message.text)
            return await self.data_collect()
        return await self.status_remove(INCORRECT_COMMAND)

    async def message_without_status(self):
        if self.message.text in EQUIPMENTS_FILTER_FIELDS:
            return await self.equipment_search()
        return await self.status_remove(INCORRECT_COMMAND)

    async def create_and_send_excel(self, equipments: list):
        dataframe = DataFrame(equipments)
        date = datetime.datetime.now().strftime(DATE_FORM)
        filepath = FILENAME.format(date=date)
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
        if self.message.text in EQUIPMENTS_FILTER_FIELDS:
            await self.send_message(
                FIND_FIELD.format(field=self.message.text),
                self.message.chat.id
            )
            return user_status.set_mapping(
                self.id, {
                    STATUS: EQUIPMENT_SEARCH,
                    STATUS_TYPE: EQUIPMENTS_FILTER_FIELDS.get(
                        self.message.text
                    )
                }
            )
        status_type = user_status.get_status_type(
            self.id
        )
        if status_type in EQUIPMENTS_FILTER_FIELDS.values():
            url = f'{status_type}={self.message.text}'
            equipments_without_formatter = await self.status_code_parser(
                self.get_api_answer(
                    url,
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
                    EQUIPMENT_ACTION_BUTTONS
                )
            if len(equipments) > MAX_COUNT:
                await self.create_and_send_excel(equipments_without_formatter)
            return user_status.delete(self.message.chat.id)
        return await self.status_remove(INCORRECT_COMMAND)

    async def status_remove(self, message):
        await self.send_message(
            message,
            self.message.chat.id,
            list(EQUIPMENTS_FILTER_FIELDS.keys())
        )
        return user_status.delete(self.message.chat.id)

    async def message_manager(self) -> None:
        if self.message.text in ('/start', QUIT.lower(), QUIT):
            return await self.status_remove(STATUS_REMOVE)
        if hasattr(self.message.reply_to_message, 'text'):
            return await self.reply_to_message_message()
        status = user_status.get_status(self.id)
        if not status:
            return await self.message_without_status()
        if status in (LOGIN, MOVEMENT_ADD):
            return await self.data_collect()
        if status in (EQUIPMENT_SEARCH,):
            return await self.equipment_search()
        return await self.status_remove(INCORRECT_COMMAND)
