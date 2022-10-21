# Laboratory equipment database with parameters and documentation on Django web UI and Telegram bot UI (in progress).

![Workflow](https://github.com/Pavelkalininn/laboratory_equipments/actions/workflows/main.yml/badge.svg)


## Description

Django - web application for operational laboratory equipment information changes.

## Technology

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

## Env file template path: 

[infra/example.env](./infra/example.env)

The DOCKER_USERNAME variable must be present in the Github secrets environment to run CI

## Project run:

### It is necessary to execute the commands in the infra folder to launch a project, apply migrations, create a superuser, load static, respectively:
    
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate
    docker-compose exec web python ./manage.py loaddata test_fixtures.json
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input

You need to register on the main page, and then confirm the user's status as staff in the admin panel to work in the web application

Run in the infra folder to stop the container:

     docker-compose down -v

To run unittest in the folder with the manage.py must be executed:

    python manage.py test


Author: [__Pavel Kalinin__](https://github.com/Pavelkalininn)
