from django.db import models


class Message(models.Model):
    """
    Модель сообщения.

    Хранит информацию о сообщении, отправленном в рамках кампании на номер клиента.

    Атрибуты:
        send_time (DateTimeField): Время отправки сообщения.
        campaign (ForeignKey): Кампания, к которой относится сообщение.
        client (ForeignKey): Клиент, которому отправлено сообщение.

    Методы:
        __str__: Возвращает строковое представление объекта сообщения.
    """

    send_time = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено в')
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='messages',
                                 verbose_name='Кампания')
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='messages',
                               verbose_name='Клиент')

    def __str__(self):
        """
        Возвращает строковое представление объекта сообщения.

        Формат: "Message {id} to {client_phone_number} at {send_time}"
        """
        return f"Сообщение {self.pk} на номер {self.client.phone_number} отправлено в {self.send_time}"
