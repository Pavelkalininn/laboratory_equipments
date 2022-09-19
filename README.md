# БД с перечнем испытательного оборудования и документацией на него

![Workflow](https://github.com/Pavelkalininn/foodgram-project-react/actions/workflows/main.yml/badge.svg)


## Описание

Для обмена рецептами необходимо залогиниться (создать аккаунт) и нажать кнопку "создать рецепт"
Для для добавления рецепта в список покупок или избранное и подписания на рецепты
автора необходимо открывать соответствующие вкладки, или на рецепте нажимать
соответствующие кнопки.

## Технологии

    Django==3.2.15
    django-filter==22.1
    django-templated-mail==1.1.1
    djangorestframework==3.13.1
    djangorestframework-simplejwt==4.8.0
    djoser==2.1.0
    drf-extra-fields==3.4.0
    filter==0.0.0.20200724
    isort==5.10.1
    Pillow==9.2.0
    python-dotenv==0.20.0
    requests==2.28.1
    psycopg2-binary==2.8.6
    gunicorn==20.0.4
    pytest==6.2.4
    pytest-django==4.4.0

## Шаблон наполнения env-файла лежит по адресу: 

[infra/example.env](./infra/example.env)
Для запуска CI необходимо наличие переменной DOCKER_USERNAME=guguruge в окружении Github secrets

## Запуск проекта:

### Для запуска проекта, применения миграций, создания суперюзера, загрузки статики и добавления в БД данных из фикстур соответственно необходимо в папке infra выполнить команды:
    
    docker-compose up -d --build
    sudo docker-compose exec backend python manage.py migrate
    sudo docker-compose exec backend python manage.py createsuperuser
    sudo docker-compose exec backend python manage.py collectstatic --no-input
    sudo docker-compose exec backend python manage.py loaddata ingredient.json

после чего будет собран и запущен контейнер, админка доступна по адресу:  

    /admin/


для остановки контейнера необходимо в папке infra выполнить:

     docker-compose down -v


## Документация с примерами запросов API доступна по адресу:

    /api/docs/


Автор: [__Паша Калинин__](https://github.com/Pavelkalininn)
