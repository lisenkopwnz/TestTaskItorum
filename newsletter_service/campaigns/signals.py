import logging

from celery.result import AsyncResult
from django.db.models.signals import post_save, post_delete
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

    Если объект кампании изменяется, задача пересоздается. Старая задача отменяется, если она находится в состоянии
    'PENDING' или 'STARTED'.

    Параметры:
        sender: Модель Campaign.
        instance: Экземпляр модели Campaign, который был сохранен.
        created: Флаг, который указывает, является ли объект новым.
        **kwargs: Дополнительные параметры, передаваемые сигналу.

    """
    if created:
        logger.info(f"Создана новая рассылка (ID: {instance.id}) с началом {instance.start_time}")

    task_id = instance.get_task_id()
    if task_id:
        existing_task = AsyncResult(task_id)
        if existing_task.state == 'PENDING' or existing_task.state == 'STARTED':
            logger.info(f"Отменяем старую задачу (ID: {task_id}) из-за изменения времени начала.")
            existing_task.revoke(terminate=True)

    if instance.start_time <= now():
        logger.info(f"Запуск рассылки (ID: {instance.id}) немедленно.")
        task = send_mailing.delay(instance.id)
        instance.set_task_id(task.id)  # Сохраняем ID задачи в объекте
    else:
        # Если время начала в будущем, запланируем задачу на это время
        logger.info(f"Рассылка (ID: {instance.id}) запланирована на {instance.start_time}.")
        task = send_mailing.apply_async((instance.id,), eta=instance.start_time)
        instance.set_task_id(task.id)  # Сохраняем ID задачи в объекте



@receiver(post_delete, sender=Campaign)
def cancel_mailing_task(sender, instance, **kwargs):
    """
    Отменяет задачу рассылки при удалении кампании, если она ещё не была выполнена.

    Логирование:
        - Если задача существует и находится в состоянии 'PENDING' или 'STARTED', она отменяется.
        - Логируется информация об отмене задачи перед удалением кампании.

    Параметры:
        sender: Модель Campaign.
        instance: Экземпляр модели Campaign, который был удален.
        **kwargs: Дополнительные параметры, передаваемые сигналу.
    """
    task_id = instance.get_task_id()

    if task_id:
        existing_task = AsyncResult(task_id)
        if existing_task.state in ['PENDING', 'STARTED']:
            logger.info(f"Отменяем задачу (ID: {task_id}) для рассылки (ID: {instance.id}) перед её удалением.")
            existing_task.revoke(terminate=True)
