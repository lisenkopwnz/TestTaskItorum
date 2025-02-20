from django.db import models
from rest_framework.exceptions import ValidationError


class Campaign(models.Model):
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    message_text = models.TextField(verbose_name="Message Text")
    operator_code_filter = models.CharField(max_length=3, verbose_name="Operator Code")
    tag_filter = models.CharField(max_length=255, verbose_name="Tag")

    def __str__(self):
        return f"Campaign id-{self.pk} - {self.start_time} to {self.end_time}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time cannot be earlier than start time")
