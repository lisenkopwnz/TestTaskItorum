import pytest
from django.utils import timezone

from client.models import Client
from message.models import Message
from campaigns.models import Campaign
from django.db.utils import IntegrityError


@pytest.mark.django_db
class TestMessageModel:

    def test_create_message(self):
        """Тестируем создание нового сообщения."""

        client = Client.objects.create(
            phone_number='+7(925)555-12-34',
            operator_code='925',
            tag='test_tag'
        )

        campaign = Campaign.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now(),
            operator_code_filter='925',
            tag_filter='test_tag'
        )

        message = Message.objects.create(
            send_time=timezone.now(),
            campaign=campaign,
            client=client
        )

        assert message.campaign == campaign
        assert message.client == client

    def test_str_method(self):
        """Тестируем строковое представление сообщения."""

        client = Client.objects.create(
            phone_number='+7(925)555-12-34',
            operator_code='925',
            tag='test_tag'
        )

        campaign = Campaign.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now(),
            operator_code_filter='925',
            tag_filter='test_tag'
        )

        message = Message.objects.create(
            send_time=timezone.now(),
            campaign=campaign,
            client=client
        )

        assert str(message) == f"Сообщение {message.id} на номер {client.phone_number} отправлено в {message.send_time}"

    def test_message_creation_without_campaign_or_client(self):
        """Тестируем создание сообщения без обязательных связей (кампания и клиент)."""

        with pytest.raises(IntegrityError):
            Message.objects.create(send_time=timezone.now())
