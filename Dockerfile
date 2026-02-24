FROM python:3.13-slim-bookworm

MAINTAINER python dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=OFF \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    COLUMNS=80

RUN apt-get update \
    && apt-get install -y \
        gcc \
        curl \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false\
    && poetry lock \
    && poetry install