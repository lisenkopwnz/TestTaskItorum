from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Message(models.Model):
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='Sent at')
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE ,related_name='messages', verbose_name='Campaign')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='messages', verbose_name='Client')

    def __str__(self):
        return f"Message {self.pk} to {self.client.phone_number} at {self.send_time}"
