#!/bin/sh

set -e

# Ждём, пока БД будет доступна
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Применяем миграции
python manage.py migrate

# Загружаем тестовые данные
python manage.py create_test_data

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000
