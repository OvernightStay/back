#!/bin/bash

# Выход при любой ошибке
set -e

# Ожидание запуска PostgreSQL
echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Переходим в директорию /app
cd /app

# Применение миграций базы данных
echo "Applying database migrations..."
python manage.py migrate

# Сборка статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запуск сервера (например, gunicorn)
echo "Starting server..."
gunicorn pro.wsgi:application --bind 0.0.0.0:8000
