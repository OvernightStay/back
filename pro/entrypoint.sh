#!/bin/sh

# Ожидание базы данных
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 5
done
echo "PostgreSQL started"

# Выполнение миграций
python manage.py migrate --noinput

# Сборка статических файлов
python manage.py collectstatic --noinput

# Запуск Gunicorn сервера
exec gunicorn --bind 0.0.0.0:8000 pro.wsgi:application
