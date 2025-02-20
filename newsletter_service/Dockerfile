# Базовый образ с Python
FROM python:3.12-slim-bullseye

# Устанавливаем переменные окружения для Python
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /newsletter_service

# Устанавливаем контейнер на UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone

# Устанавливаем netcat (nc), чтобы исправить ошибку
RUN apt-get update && apt-get install -y netcat

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Копируем entrypoint.sh и делаем его исполнимым
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Открываем порт для приложения (по умолчанию Django на 8000)
EXPOSE 8000

# Команда для запуска Django приложения
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]