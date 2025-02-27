# Сервис управления рассылками

Этот проект представляет собой сервис для управления рассылками сообщений клиентам. Он позволяет создавать новые рассылки, просматривать их и автоматически отправлять сообщения соответствующим клиентам в указанное время.

## Описание

Сервис выполняет следующие функции:

- Создание новой рассылки с заданием времени старта и окончания, текста сообщения, а также фильтра по клиентам (мобильный оператор, тег).
- Автоматическое выполнение рассылки, если текущее время находится в пределах указанного времени старта и окончания.
- Просмотр всех созданных рассылок.
- Отправка сообщений клиентам, соответствующим фильтрам рассылки, с выводом сообщений в консоль.

### Сущности:

1. **Рассылка**:
   - Уникальный id рассылки.
   - Время старта и окончания рассылки.
   - Текст сообщения.
   - Фильтр по клиентам (код мобильного оператора, тег).
   - Приватное поле для хранения ID задачи Celery, связанной с этой рассылкой.
   
2. **Клиент**:
   - Уникальный id клиента.
   - Номер телефона клиента в формате `7XXXXXXXXXX`.
   - Код мобильного оператора.
   - Тег.
   
3. **Сообщение**:
   - Уникальный id сообщения.
   - Дата и время отправки.
   - id рассылки, в рамках которой было отправлено сообщение.
   - id клиента, которому было отправлено сообщение.

# Особенности работы:

- Если текущее время находится в пределах времени старта и окончания рассылки, сообщения отправляются всем клиентам, 
соответствующим фильтрам (по оператору и тегу).
- Если время рассылки истекло или не попадает в допустимый интервал, задача не будет выполнена.
- При ошибках отправки сообщений задача Celery повторяется с экспоненциальной задержкой, что обеспечивает надежность системы.
- Если объект кампании изменяется (например, время старта или другие параметры), задача пересоздается
- Старая задача отменяется, если она находится в состоянии PENDING или STARTED. Это гарантирует, что задачи не будут выполняться в случае изменения условий кампании.
- После отмены старой задачи создается новая задача, привязанная к измененному объекту кампании.
- Это предотвращает выполнение задач, привязанных к удаленным кампаниям, и очищает очередь.

## Тесты
- Запускаются из контейнера приложения командой pytest

## Установка и запуск

### Требования:
- Docker
- Docker Compose

### 1. Клонировать репозиторий:


git clone https://github.com/lisenkopwnz/TestTaskItorum

cd newsletter-service

### 2. Создание файла .env
Для настройки приложения, создайте файл `.env` в корневой директории 
,иначе будут действовать следующие настройки:


# PostgreSQL settings
DB_NAME=mydatabase,
DB_USER=myuser,
DB_PASSWORD=mypassword,
DB_HOST=db,
DB_PORT=5432,

# Celery settings
CELERY_BROKER_URL=redis://redis:6379/0,
CELERY_RESULT_BACKEND=redis://redis:6379/0,
CELERY_ACCEPT_CONTENT=json,
CELERY_TASK_SERIALIZER=json,
CELERY_RESULT_SERIALIZER=json,
CELERY_TIMEZONE=UTC,

# Redis settings
REDIS_HOST=redis,
REDIS_PORT=6379

# Web server settings
WEB_HOST=0.0.0.0,
WEB_PORT=8000


### 3. Сборка и запуск с использованием Docker:
Для сборки и запуска приложения выполните следующую команду:

docker-compose up --build

### 4. Проверка API через Postman:
- Коллекция Postman для тестирования API находится в директории `postman` проекта.
- Импортируйте коллекцию из файла в Postman, чтобы протестировать все доступные API-методы.

## Важные моменты:
- Все временные данные записываются в формате ISO 8601, например: `2025-02-22T05:25:00Z`, 
- где "Z" указывает на то, что время представлено в UTC.

## Проверка номеров

В проекте реализована **проверка номеров** в соответствии с актуальными правилами России. Это включает в себя:
- Валидацию формата номеров мобильных телефонов, соответствующего стандартам России.
- Проверку, что номер состоит из 11 цифр, начинающихся с кода страны `+7`.
- Дополнительную проверку на корректность введённых данных в формате мобильных номеров для предотвращения ошибок.

**Пример валидного номера:**
- `+7 912 345 67 89`

Все эти проверки реализованы в соответствии с национальными стандартами и требованиями.
