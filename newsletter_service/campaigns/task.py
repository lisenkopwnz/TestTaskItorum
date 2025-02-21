import logging

from celery import shared_task
from django.utils.timezone import now

from campaigns.models import Campaign
from client.models import Client
from message.models import Message


logger = logging.getLogger('console_log')

@shared_task(bind=True, max_retries=5, default_retry_delay=10, retry_backoff=True, retry_backoff_max=300)
def send_mailing(self, mailing_id):
    """Задача отправки рассылки с экспоненциальной задержкой"""
    try:
        mailing = Campaign.get(id=mailing_id)
        current_time = now()

        # Проверяем, что текущее время находится в пределах допустимого интервала рассылки
        if mailing.start_time <= current_time <= mailing.end_time:
            logger.info(f"Запуск рассылки {mailing.id}: время в пределах допустимого интервала.")

            # Используем правильное имя поля для operator_code
            clients = Client.filter(
                operator_code=mailing.operator_code_filter,
                tag=mailing.tag_filter
            )

            for client in clients:
                # Прерываем рассылку, если время завершения прошло
                if now() > mailing.end_time:
                    logger.warning(f"Время рассылки {mailing.id} истекло для клиента {client.phone_number}."
                                   f"Прекращаем рассылку.")
                    break

                # Имитация отправки сообщения
                logger.info(f"Отправка: {mailing.message_text} -> {client.phone_number}")
                Message.objects.create(
                    campaign=mailing,
                    client=client,
                    send_time=now()
                )

        else:
            logger.warning(f"Время рассылки {mailing.id} не в пределах допустимого интервала."
                           f"Текущее время: {current_time}, Время начала: {mailing.start_time},"
                           f"Время окончания: {mailing.end_time}")

    except Campaign.DoesNotExist:
        logger.error(f"Рассылка с id {mailing_id} не найдена.")
    except Exception as e:
        logger.error(f"Произошла ошибка при отправке рассылки {mailing_id}: {e}")
        # Если что-то пошло не так, повторяем задачу с экспоненциальной задержкой
        raise self.retry(exc=e)
