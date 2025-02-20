#!/bin/bash

# Ожидание запуска Redis
echo "Ожидание запуска Redis на $REDIS_HOST:$REDIS_PORT..."
timeout=240
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: Redis не запустился за ожидаемое время."
        exit 1
    fi
done

echo "Redis доступен."

# Ожидание запуска веб-приложения
echo "Ожидание запуска веб-приложения на $WEB_HOST:$WEB_PORT..."
timeout=240
while ! nc -z $WEB_HOST $WEB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: Веб-приложение не запустилось за ожидаемое время."
        exit 1
    fi
done

echo "Веб-приложение доступно."

# Запуск Celery
exec "$@"