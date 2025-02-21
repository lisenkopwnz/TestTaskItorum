from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


class Client(models.Model):
    """
    Модель клиента.

    Содержит информацию о номере телефона клиента, коде оператора и теге для фильтрации.

    Атрибуты:
        phone_number (PhoneNumberField): Уникальный номер телефона клиента в формате E.164.
        operator_code (CharField): Код оператора связи (необязательное поле, заполняется автоматически).
        tag (CharField): Тег клиента, используемый для фильтрации (необязательное поле).
    """

    phone_number = PhoneNumberField(unique=True, region='RU', verbose_name='Номер телефона')
    operator_code = models.CharField(max_length=3, verbose_name='Код оператора', blank=True)
    tag = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тег клиента')

    def __str__(self):
        """
        Возвращает строковое представление объекта клиента.

        Формат: "Клиент id-{id}, номер телефона-{phone_number}"
        """
        return f'Клиент id-{self.pk}, номер телефона-{self.phone_number}'

    def save(self, *args, **kwargs):
        """
        Переопределенный метод save.

        Если код оператора не указан, вычисляется автоматически с помощью метода `calculate_operator_code()`.
        """
        if not self.operator_code:
            self.operator_code = self.calculate_operator_code()
        super().save(*args, **kwargs)

    def calculate_operator_code(self):
        """
        Логика вычисления кода оператора.

        Извлекает первые три цифры после кода страны из номера телефона.

        Пример:
            Для номера +7(911)123-45-67 операторский код будет "911".
        """
        phone_number_str = str(self.phone_number)
        operator_code = phone_number_str[2:5]
        return operator_code

    @classmethod
    def filter(cls, **kwargs):
        """
        Класс-метод для получения кампаний по заданным фильтрам.
        Возвращает QuerySet с найденными кампаниями. Если ничего не найдено, выбрасывает исключение.
        """
        campaigns = cls.objects.filter(**kwargs)

        if not campaigns.exists():
            raise ValidationError("Клиент не найден.")

        return campaigns
