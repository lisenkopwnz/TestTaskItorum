from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    phone_number = PhoneNumberField(unique=True, region='RU', verbose_name='Phone number')
    operator_code = models.CharField(max_length=3, verbose_name='Operator code')
    tag = models.CharField(max_length=255, blank=True, null=True, verbose_name='Client tag')

    def __str__(self):
        return f'Client id-{self.pk}, phone number-{self.phone_number}'
