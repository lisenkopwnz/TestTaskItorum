from __future__ import absolute_import, unicode_literals

# Импортируем app из celery.py
from .celery_config import app as celery_app

__all__ = ('celery_app',)