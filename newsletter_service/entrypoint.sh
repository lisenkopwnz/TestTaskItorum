#!/bin/bash

# Ожидание запуска PostgreSQL
echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."
timeout=240

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: PostgreSQL не запустился за отведённое время."
        exit 1
    fi
done

echo "PostgreSQL запущен. Начинаем подготовку приложения..."

# Ожидание запуска Redis
echo "Ожидание запуска Redis на $REDIS_HOST:$REDIS_PORT..."
timeout=240

while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: Redis не запустился за отведённое время."
        exit 1
    fi
done

echo "Redis запущен. Продолжаем..."

# Создание миграций
echo "Создание миграций..."
if ! python manage.py makemigrations; then
    echo "Ошибка: не удалось создать миграции"
    exit 1
fi

# Применение миграций
echo "Применение миграций..."
if ! python manage.py migrate --noinput; then
    echo "Ошибка: не удалось применить миграции"
    exit 1
fi

# Запуск приложения Django
echo "Запуск приложения Django..."
python manage.py runserver 0.0.0.0:8000 &

# Запуск Celery worker
echo "Запуск Celery worker..."
celery -A newsletter_service worker --loglevel=info -Q work_queue &

# Ожидание всех процессов
wait -n