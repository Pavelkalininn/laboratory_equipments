import os

from dotenv import (
    load_dotenv,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEB_HOST = os.getenv('WEB_HOST')
REDIS_HOST = os.getenv('REDIS_HOST')
ADMIN_ID = int(os.getenv('TELEGRAM_TO'))
WEB_URL = os.getenv('WEB_URL')
API_PORT = os.getenv('API_PORT')
MAX_COUNT = 10
STATUS = 'status'
STATUS_TYPE = 'status_type'

TOO_MANY_RESULTS = f'''
Слишком много результатов, будут показаны первые {MAX_COUNT},
 попробуйте усложнить критерии поиска или работать с web версией, весь список в прикрепленном excel!
'''
FIND_FIELD = 'Ищем по полю {field}, введите значение'
FILL_IN_VALUE = 'Введите {value}'
ADMIN_ADD_OR_DELETE_YOU = '''
Ваш пользователь {added_or_deleted} в список персонала.
 Теперь доступны все функции.
'''
ADDED = 'добавлен'
QUIT = 'Сброс'
DELETED = 'удалён'
USER_SUCCESSFULLY_ADD_OR_DELETE = 'Пользователь успешно {added_or_deleted}'
SUCCESSFULLY_CREATED = 'Успешно создан!'
EQUIPMENTS = 'Оборудование'
LOGIN = 'регистрация'
EQUIPMENT_ADD = 'Добавить оборудование'
MOVEMENT_ADD = 'Передать оборудование'
EQUIPMENT_SEARCH = 'Поиск оборудования'
EQUIPMENT_CHANGE = 'Изменить оборудование'
STAFF_ACCEPT = 'Подтвердить сотрудника'
STAFF_DECLINE = 'Отменить статус сотрудника'
EDIT = 'Изменить'
TODAY = 'Сегодня'
DASH = '-'
PASS_VALUES = [DASH, TODAY]
DATE_FORM = '%y_%d_%m_%H_%M'
FILENAME = 'equipment_list_{date}.xlsx'
EXCEL_HEADERS = [
    'id',
    'Инвентарный номер',
    'Наименование',
    'Модель',
    'Код ТН ВЭД',
    'Руководство по эксплуатации',
    'Путь к папке с документами',
    'Место нахождения',
    'Создатель'

]

EQUIPMENT_CHANGE_INFO = '''
Для изменения оборудования необходимо сначала найти его, а затем в ответе на
 сообщение с его id нажать кнопку Изменить оборудование!'''

INCORRECT_COMMAND = (
    'Введенная команда не используется, необходимо выбрать команду из '
    'предложенных вариантов'
)
ACCESS_DENIED = 'Ошибка доступа, пользователь не найден 403'
INCORRECT_STATUS = 'Некорректный статус от API {status}'

AUTHORIZATION = 'Authorization'
STATUS_REMOVE = 'Залезли в какие-то дебри, начнём сначала. Статус сбросили.'
INFO = '''
Бот для просмотра и внесения сведений по оборудованию

'''
BUTTON_START = ['/start']
EQUIPMENT_ACTION_BUTTONS = (QUIT, MOVEMENT_ADD)
ANY_THINK_WAS_WRONG = (
    'Что-то пошло не так, если ошибка повторится - обратитесь к администратору'
)
NO_ONE_OBJECT_FIND = 'Не найдено ни одного подходящего объекта'
INPUT_VALUE = 'Введите значение'
EQUIPMENTS_FILTER_FIELDS = {
    'Наименование': 'name',
    'Инвентарный номер': 'inventory',
    'Модель': 'model',
    'Код ТН ВЭД ЕАЭС': 'nomenclature_key',
    'Местонахождение': 'movement'
}
UNAUTHORIZED = (
    '401 Ошибка доступа, обратитесь к администратору для доступа'
    ' к служебной информации'
)
USER_FORM = (
    '''
Пользователь {username}

с электронной почтой {email}
именем {first_name}
фамилией {last_name}
и телеграм id {telegram_id}
статус персонала: {is_staff}

Успешно создан!
Для доступа к служебной информации перешлите это сообщение и/или обратитесь к администратору.
До тех пор, пока администратор не добавит Вас в список персонала, будет ошибка 401
Для работы с Web версией перейдите по ссылке '''
    + WEB_URL
    + ''' находясь в локальной сети (можно через VPN) Связь-сертификат.
Опять же не будет работать, пока админ не добавит юзера в статус персонала.
'''
)
EQUIPMENT_CONST = (
    '''id: {id}
Инвентарный номер: {inventory}

Наименование: {name}
Модель: {model}
Код ТН ВЭД: {nomenclature_key}
Путь к папке с документами: {document_path}
Местоположения: {movements}

Последнее изменение пользователем: {creator}
'''
)

MOVEMENT_CREATE_NAMES = {
    'date': 'Дата (если не текущей)',
    'recipient': 'Фамилия получателя',
    'destination': 'Место назначения'
}
USER_CREATE_NAMES = {
    'email': 'электронную почту',
    'first_name': 'имя',
    'last_name': 'фамилию',
    'username': 'имя пользователя (на латинице)',
    'password': 'пароль (не менее 8-ми символов, не менее одного из которых заглавная буква, не совпадающий с логином)'
}
