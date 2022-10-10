# БД с перечнем испытательного оборудования лаборатории с документацией на него

![Workflow](https://github.com/Pavelkalininn/laboratory_equipments/actions/workflows/main.yml/badge.svg)


## Описание

Django - web приложение для оперативного изменения информации по оборудованию ИЛ

## Технологии

    Django==3.2.15
    django-filter==22.1
    django-templated-mail==1.1.1
    djangorestframework==3.13.1
    djangorestframework-simplejwt==4.8.0
    djoser==2.1.0
    PyJWT==2.4.0
    python-dotenv==0.20.0
    requests==2.28.1
    gunicorn==20.1.0
    psycopg2-binary==2.9.3

## Шаблон наполнения env-файла лежит по адресу: 

[infra/example.env](./infra/example.env)
Для запуска CI необходимо наличие переменной DOCKER_USERNAME в окружении Github secrets

## Запуск проекта:

### Для запуска проекта, применения миграций, создания суперюзера, загрузки статики соответственно необходимо в папке infra выполнить команды:
    
    sudo docker-compose up -d --build
    sudo docker-compose exec web python manage.py migrate
    sudo docker-compose exec web python manage.py createsuperuser
    sudo docker-compose exec web python manage.py collectstatic --no-input

Для работы в приложении необходимо зарегистрироваться на главной странице, после чего подтвердить статус пользователя как staff в админ-панели

для остановки контейнера необходимо в папке infra выполнить:

     docker-compose down -v

Для запуска тестов unittest в корневой папке необходимо выполнить:

    sudo docker-compose -f ./infra/docker-compose_tests.yml up -d --build
    sudo docker-compose -f ./infra/docker-compose_tests.yml exec -T web python manage.py test


Автор: [__Паша Калинин__](https://github.com/Pavelkalininn)
