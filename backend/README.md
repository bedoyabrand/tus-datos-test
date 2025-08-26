# ----------------------
# 1. Build stage
# ----------------------
FROM python:3.12-slim AS builder

# Evitar buffer en logs y establecer working dir
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Instala dependencias básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copia archivos de dependencias primero para cache
COPY pyproject.toml poetry.lock* ./

# Instala dependencias de producción
RUN poetry install --no-dev --no-interaction --no-ansi

# ----------------------
# 2. Runtime stage
# ----------------------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copia dependencias desde builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /root/.local /root/.local

# Copia el código de la app y alembic
COPY app ./app
COPY alembic.ini .
COPY alembic ./alembic

# Copia también los tests (para poder correr pytest dentro del contenedor si quieres)
COPY tests ./tests

# Puerto donde corre FastAPI
EXPOSE 8000

# Comando de inicio por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
