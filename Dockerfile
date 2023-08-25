FROM python:3.10-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    WORKDIR_PATH=/app

WORKDIR $WORKDIR_PATH

RUN curl -sSL https://install.python-poetry.org | python

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src/ $WORKDIR_PATH

WORKDIR /app/src
