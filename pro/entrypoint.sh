#!/bin/sh

# Ожидание запуска базы данных
echo "Waiting for postgres to start..."
while ! pg_isready -h db -p 5432 -q; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done
echo "Postgres is ready"

# Выполнение миграций
python manage.py migrate --noinput

# Сборка статических файлов
python manage.py collectstatic --noinput

# Запуск Gunicorn сервера
exec gunicorn --bind 0.0.0.0:8000 pro.wsgi:application
