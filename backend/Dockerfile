FROM python:3.12-slim

# Evita buffering de logs
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_CREATE=false

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl tzdata git && \
    rm -rf /var/lib/apt/lists/*

# Instalar Poetry
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copiar descriptors primero para caché
COPY pyproject.toml ./
RUN poetry install --no-interaction --no-ansi

# Copiar código
COPY app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

EXPOSE 8000
