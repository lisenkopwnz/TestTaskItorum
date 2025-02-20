from celery import shared_task
from django.utils.timezone import now

from campaigns.models import Campaign
from client.models import Client
from message.models import Message


@shared_task(bind=True, max_retries=5, default_retry_delay=10, retry_backoff=True, retry_backoff_max=300)
def send_mailing(self, mailing_id):
    """Задача отправки рассылки с экспоненциальной задержкой"""
    try:
        mailing = Campaign.objects.get(id=mailing_id)
        current_time = now()

        # Проверяем, что текущее время находится в пределах допустимого интервала рассылки
        if mailing.start_time <= current_time <= mailing.end_time:
            clients = Client.objects.filter(
                operator_code=mailing.operator_code,
                tag=mailing.tag
            )

            for client in clients:
                # Прерываем рассылку, если время завершения прошло
                if now() > mailing.end_time:
                    print(f"Время рассылки истекло. Прекращаем отправку.")
                    break  # Прерываем цикл отправки сообщений

                # Имитация отправки сообщения
                print(f"Отправка: {mailing.text} -> {client.phone_number}")
                Message.objects.create(
                    mailing=mailing,
                    client=client,
                    sent_at=now()
                )
        else:
            print("Время рассылки не в пределах допустимого интервала.")

    except Campaign.DoesNotExist:
        print("Рассылка не найдена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Если что-то пошло не так, повторяем задачу с экспоненциальной задержкой
        raise self.retry(exc=e)  # Повторить задачу с ошибкой
