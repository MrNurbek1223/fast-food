FROM python:3.12-alpine

LABEL maintainer="@pedbad"

ENV PYTHONUNBUFFERED 1


RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    gdal-dev \
    geos-dev \
    proj-dev \
    bash







ENV LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH


COPY . /core

# Ishchi katalogni belgilash
WORKDIR /core
RUN export $(cat /core/.env | xargs)
# Virtual environment yaratish va paketlarni o'rnatish
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /core/requirements.txt

# Ortiqcha fayllarni o'chirish
RUN rm -rf /core && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# PATH ga virtual environment yo'lini qo'shish
ENV PATH="/venv/bin:$PATH"

# Django foydalanuvchisi sifatida ishlash
USER django-user


EXPOSE 8000
