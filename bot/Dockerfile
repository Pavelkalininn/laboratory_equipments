FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py"]