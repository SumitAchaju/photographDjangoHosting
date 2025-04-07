FROM python:3.12.1-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev 

RUN pip install --upgrade pip  && \
    python3 -m pip install  --no-cache-dir -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput

# Build the final image
FROM python:3.12.1-alpine


RUN apk add --no-cache \
    libpq \
    libjpeg \
    zlib

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app


