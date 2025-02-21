import pytest
from rest_framework import status
from client.models import Client
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestClientViewSet:

    def setup_method(self):
        """Подготовка теста: создание клиента и APIClient."""
        self.client = APIClient()
        self.client_data = {
            'phone_number': '+7(911)123-45-67',
            'operator_code': '911',
            'tag': 'test_tag'
        }

        self.client_instance = Client.objects.create(**self.client_data)

    def test_create_client(self):
        """Тестируем создание нового клиента."""
        new_client_data = {
            'phone_number': '+7(925)456-78-90',
            'operator_code': '925',
            'tag': 'new_tag'
        }
        response = self.client.post('/client/api/', new_client_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        normalized_phone_number = '+79254567890'
        assert response.data['phone_number'] == normalized_phone_number

    def test_update_client(self):
        """Тестируем полное обновление данных клиента."""
        updated_data = {
            'phone_number': '+7(911)987-65-43',
            'operator_code': '911',
            'tag': 'updated_tag'
        }
        response = self.client.put(f'/client/api/{self.client_instance.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        normalized_phone_number = '+79119876543'
        assert response.data['phone_number'] == normalized_phone_number

    def test_partial_update_client(self):
        """Тестируем частичное обновление данных клиента."""
        partial_update_data = {'tag': 'partial_updated_tag'}
        response = self.client.patch(f'/client/api/{self.client_instance.id}/', partial_update_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['tag'] == partial_update_data['tag']

    def test_delete_client(self):
        """Тестируем удаление клиента."""
        response = self.client.delete(f'/client/api/{self.client_instance.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Client.objects.filter(id=self.client_instance.id).exists()
