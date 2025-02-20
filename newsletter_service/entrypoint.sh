#!/bin/bash

# Ожидание запуска PostgreSQL
echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."
timeout=240

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: PostgreSQL не запустился за ожидаемое время."
        exit 1
    fi
done

echo "PostgreSQL доступен."

# Автоматическое создание миграций и их применение
echo "Применяю миграции..."
if ! python manage.py makemigrations; then
    echo "Ошибка: Не удалось создать миграции"
    exit 1
fi

if ! python manage.py migrate; then
    echo "Ошибка: Не удалось применить миграции"
    exit 1
fi

exec "$@"
