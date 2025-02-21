import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from campaigns.models import Campaign
from client.models import Client
from message.models import Message


@pytest.mark.django_db
class TestMessageViewSet:
    """Тесты для MessageViewSet (ReadOnlyModelViewSet)"""

    @pytest.fixture
    def campaign(self):
        """Фикстура для создания кампании"""
        return Campaign.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
            message_text="Тестовое сообщение",
            operator_code_filter="911",
            tag_filter="test_tag"
        )

    @pytest.fixture
    def client(self):
        """Фикстура для создания клиента"""
        return Client.objects.create(
            phone_number="+79111234567",
            operator_code="911",
            tag="test_tag"
        )

    @pytest.fixture
    def message(self, campaign, client):
        """Фикстура для создания сообщения"""
        return Message.objects.create(
            campaign=campaign,
            client=client
        )

    @pytest.fixture
    def api_client(self):
        """Фикстура для создания API клиента"""
        return APIClient()

    def test_get_message_list(self, api_client):
        """Тест для получения списка сообщений"""
        url = reverse('message-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
