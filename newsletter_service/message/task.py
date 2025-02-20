from django.utils.timezone import now

from message.models import Campaign, Client, Message


@shared_task
def send_mailing(mailing_id):
    """Задача отправки рассылки"""
    try:
        mailing = Campaign.objects.get(id=mailing_id)
        if mailing.start_time <= now() <= mailing.end_time:
            clients = Client.objects.filter(
                operator_code=mailing.operator_code,
                tag=mailing.tag
            )
            for client in clients:
                # Имитация отправки сообщения (можно заменить реальной логикой)
                print(f"Отправка: {mailing.text} -> {client.phone_number}")
                Message.objects.create(
                    mailing=mailing,
                    client=client,
                    sent_at=now()
                )
        else:
            print("Время рассылки истекло или ещё не наступило.")
    except Campaign.DoesNotExist:
        print("Рассылка не найдена.")