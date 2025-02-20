from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings  # Импортируем настройки Django

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletter_service.settings')

# Создаем объект Celery
app = Celery('newsletter_service')

# Загружаем конфигурацию Celery из настроек Django (settings.py)
app.config_from_object('django.conf:settings', namespace='CELERY_')

# Автоматически ищем задачи в приложениях Django
app.autodiscover_tasks()

# Если нужно настроить обработку ошибок или другие параметры
app.conf.update(
    task_default_queue='default',
    result_backend=settings.CELERY_RESULT_BACKEND,
)
