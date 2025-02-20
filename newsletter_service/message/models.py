from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone




class Campaign(models.Model):
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    message_text = models.TextField(verbose_name="Message Text")
    operator_code_filter = models.CharField(max_length=3, verbose_name="Operator Code")
    tag_filter = models.CharField(max_length=255, verbose_name="Tag")

    def __str__(self):
        return f"Campaign id-{self.pk} - {self.start_time} to {self.end_time}"

class Message(models.Model):
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='Sent at')
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE ,related_name='messages', verbose_name='Campaign')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='messages', verbose_name='Client')

    def __str__(self):
        return f"Message {self.pk} to {self.client.phone_number} at {self.send_time}"
