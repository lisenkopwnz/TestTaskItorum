import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .task import send_mailing
from campaigns.models import Campaign

logger = logging.getLogger('console_log')

@receiver(post_save, sender=Campaign)
def schedule_mailing(sender, instance, created, **kwargs):
    """
    Запускает рассылку немедленно, если время начала уже наступило,
    или планирует её на будущее с помощью Celery.

    Логирование:
    - Информация о создании новой рассылки.
    - Немедленный запуск рассылки, если время начала уже наступило.
    - Отложенный запуск, если время начала в будущем.
    """
    if created:
        logger.info(f"Создана новая рассылка (ID: {instance.id}) с началом {instance.start_time}")

        if instance.start_time <= now():
            logger.info(f"Запуск рассылки (ID: {instance.id}) немедленно.")
            send_mailing.delay(instance.id)
        else:
            logger.info(f"Рассылка (ID: {instance.id}) запланирована на {instance.start_time}.")
            send_mailing.apply_async((instance.id,), eta=instance.start_time)
