import pytest
from rest_framework import status
from rest_framework.test import APIClient
from campaigns.models import Campaign
from django.utils import timezone

@pytest.fixture
def campaign_data():
    """Фикстура для создания данных рассылки."""
    return {
        'start_time': timezone.now(),
        'end_time': timezone.now() + timezone.timedelta(days=1),
        'message_text': 'Test message',
        'operator_code_filter': '123',
        'tag_filter': 'test_tag',
    }

@pytest.fixture
def create_campaign(campaign_data):
    """Фикстура для создания самой рассылки в базе данных."""
    return Campaign.objects.create(**campaign_data)

@pytest.mark.django_db
class TestMailingViewSet:
    def setup_method(self):
        self.client = APIClient()

    def test_get_campaign_list(self, create_campaign):
        """Тестирует получение списка кампаний."""
        response = self.client.get('/campaign/api/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Т.к. мы создали одну кампанию в фикстуре

    def test_get_campaign_detail(self, create_campaign):
        """Тестирует получение конкретной кампании по ID."""
        response = self.client.get(f'/campaign/api/{create_campaign.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == create_campaign.id

    def test_create_campaign(self, campaign_data):
        """Тестирует создание новой кампании."""
        response = self.client.post('/campaign/api/', campaign_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message_text'] == campaign_data['message_text']
        assert 'id' in response.data  # Проверка, что id кампании возвращается

    def test_update_campaign(self, create_campaign):
        """Тестирует обновление существующей кампании."""
        updated_data = {
            'message_text': 'Updated message',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(days=2),
            'operator_code_filter': '321',
            'tag_filter': 'updated_tag'
        }
        response = self.client.put(f'/campaign/api/{create_campaign.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message_text'] == updated_data['message_text']

    def test_partial_update_campaign(self, create_campaign):
        """Тестирует частичное обновление существующей кампании."""
        partial_data = {'message_text': 'Partially updated message'}
        response = self.client.patch(f'/campaign/api/{create_campaign.id}/', partial_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message_text'] == partial_data['message_text']

    def test_delete_campaign(self, create_campaign):
        """Тестирует удаление кампании."""
        response = self.client.delete(f'/campaign/api/{create_campaign.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Проверим, что кампания была удалена
        response_get = self.client.get(f'/campaign/api/{create_campaign.id}/')
        assert response_get.status_code == status.HTTP_404_NOT_FOUND
        