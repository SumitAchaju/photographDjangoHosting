FROM python:3.12.1-alpine

ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_PASSWORD
ARG DJANGO_SUPERUSER_EMAIL

ENV DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
ENV DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
ENV DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL



WORKDIR /app

COPY requirements.txt .

RUN \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt 

COPY . .

RUN sh entrypoint.sh

