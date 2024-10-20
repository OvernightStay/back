#!/bin/sh

# Ожидание запуска базы данных
echo "Waiting for postgres to start..."
while ! pg_isready -h db -p 5432 -q; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done
echo "Postgres is ready"

# Выполнение команды makemigrations перед миграциями
echo "Making migrations..."
python manage.py makemigrations

# Выполнение миграций
echo "Applying migrations..."
python manage.py migrate --noinput

# Сборка статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запуск Gunicorn сервера
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 pro.wsgi:application
