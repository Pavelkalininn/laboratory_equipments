import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEB_HOST = os.getenv('WEB_HOST')
ADMIN_ID = int(os.getenv('TELEGRAM_TO'))
MAX_COUNT = 10

LOGIN = 'регистрация'
EQUIPMENT_ADD = 'Добавить оборудование'
EQUIPMENT_SEARCH = 'Поиск оборудования'
EQUIPMENT_CHANGE = 'Изменить оборудование'
STAFF_ACCEPT = 'Подтвердить сотрудника'
STAFF_DECLINE = 'Отменить статус сотрудника'

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
    # EQUIPMENT_CHANGE:
    #     [[], 'Введите инвентарный номер / наименование оборудования'],
    EQUIPMENT_ADD:
        [[], 'Введите инвентарный номер']

}
INCORRECT_COMMAND = (
    'Введенная команда не используется, необходимо выбрать команду из '
    'предложенных вариантов'
)
INFO = '''
Бот для просмотра и внесения сведений по оборудованию

'''
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

USER_FORM = '''
Пользователь {username}

с электронной почтой {email}
именем {first_name}
фамилией {last_name}
и телеграм id {telegram_id} 
статус персонала: {is_staff}

Успешно создан!
Для доступа к служебной информации перешлите это сообщение
 и/или обратитесь к администратору.
До тех пор, пока администратор не добавит Вас в список персонала,
 будет ошибка 401
Для работы с Web версией перейдите по ссылке http://192.168.1.175/
 находясь в локальной сети (можно через VPN) Связь-сертификат.
Опять же не будет работать, пока админ не добавит юзера в статус персонала.
'''
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
USER_CREATE_NAMES = [
    ('email', 'электронную почту'),
    ('first_name', 'имя'),
    ('last_name', 'фамилию'),
    ('username', 'имя пользователя (на латинице)'),
    ('password', 'пароль')
]
