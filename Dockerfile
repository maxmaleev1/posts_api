# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

COPY pyproject.toml poetry.lock README.md /app/

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем entrypoint
COPY entrypoint.sh /app/entrypoint.sh

# Делаем его исполняемым
RUN chmod +x /app/entrypoint.sh

# Устанавливаем точку входа
ENTRYPOINT ["/app/entrypoint.sh"]
