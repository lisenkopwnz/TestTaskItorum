from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from message.models import Campaign


@receiver(post_save, sender=Campaign)
def schedule_mailing(sender, instance, created, **kwargs):
    """Запускает рассылку сразу или планирует на будущее"""
    if created:  # Чтобы не запускалось при обновлении
        if instance.start_time <= now():
            send_mailing.delay(instance.id)
        else:
            send_mailing.apply_async((instance.id,), eta=instance.start_time)