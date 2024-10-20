# Используем официальный Python образ
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat-openbsd \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости перед копированием кода проекта (для кэширования)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY pro/ /app/

# Копируем скрипт entrypoint
COPY pro/entrypoint.sh /entrypoint.sh

# Делаем скрипт исполняемым
RUN chmod +x /entrypoint.sh

# Expose порт Gunicorn
EXPOSE 8000

# Указываем скрипт в качестве точки входа
ENTRYPOINT ["/entrypoint.sh"]
