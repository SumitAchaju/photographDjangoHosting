FROM python:3.12.1-alpine


WORKDIR /app

COPY requirements.txt .

RUN \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt 

COPY . .

RUN python3 manage.py makemigrations && \
    python3 manage.py migrate