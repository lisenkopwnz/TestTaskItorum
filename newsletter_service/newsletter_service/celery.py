from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletter_service.settings')

app = Celery('newsletter_service')

app.config_from_object('django.conf:settings', namespace='CELERY_')

app.autodiscover_tasks()

app.conf.update(
    task_default_queue='default',
    result_backend=settings.CELERY_RESULT_BACKEND,
)
