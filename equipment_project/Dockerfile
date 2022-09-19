FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir

COPY .. .

CMD ["gunicorn", "equipment_project.wsgi:application", "--bind", "0:8000" ]