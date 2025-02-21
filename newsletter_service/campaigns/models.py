from django.db import models
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


class Campaign(models.Model):
    """
    Модель маркетинговой кампании.

    Описывает параметры кампании, включая период действия, текст сообщения и фильтры
    по оператору и тегу.

    Атрибуты:
        start_time (DateTimeField): Дата и время начала кампании.
        end_time (DateTimeField): Дата и время окончания кампании.
        message_text (TextField): Текст сообщения, которое будет отправлено клиентам.
        operator_code_filter (CharField): Код оператора.
        tag_filter (CharField): Тег для фильтрации получателей.

    Валидация:
        - Дата окончания не может быть раньше даты начала.
        - Дата начала не может быть в прошлом.
        - Дата окончания не может быть в прошлом.

    Методы:
        __str__: Возвращает строковое представление кампании.
        clean: Проверяет корректность дат перед сохранением.

    Исключения:
        ValidationError: Выбрасывается при нарушении условий валидации.
    """

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    message_text = models.TextField(verbose_name="Текст сообщения")
    operator_code_filter = models.CharField(max_length=3, verbose_name="Код оператора")
    tag_filter = models.CharField(max_length=255, verbose_name="Тег")

    def __str__(self):
        return f"Рассылка ID-{self.pk} - {self.start_time} до {self.end_time}"

    def clean(self):
        """
        Проверяет корректность введенных данных перед сохранением:
        - Дата окончания не может быть раньше даты начала.
        - Дата начала не может быть в прошлом.
        - Дата окончания не может быть в прошлом.

        Если одно из условий не выполняется, выбрасывается ValidationError.
        """
        if self.end_time <= self.start_time:
            raise ValidationError("Дата окончания не может быть раньше даты начала.")

        if self.start_time < now():
            raise ValidationError("Дата начала не может быть в прошлом.")

        if self.end_time < now():
            raise ValidationError("Дата окончания не может быть в прошлом.")

    @classmethod
    def get(cls, **kwargs):
        """
            Класс-метод для получения кампании по заданным фильтрам.
            Этот метод позволяет искать кампанию по любому набору переданных параметров.
            Параметры передаются через `**kwargs`, что позволяет гибко фильтровать объекты модели.
        """
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            raise ValidationError(f"Рассылка не найдена.")
