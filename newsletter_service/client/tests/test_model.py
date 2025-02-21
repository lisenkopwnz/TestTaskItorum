import pytest

from phonenumber_field.phonenumber import PhoneNumber

from client.models import Client


@pytest.mark.django_db
class TestClient:

    def test_create_client_without_operator_code(self):
        """Тестирует создание клиента без указания кода оператора."""

        phone_number = "+7(911)123-45-67"
        client = Client.objects.create(
            phone_number=phone_number,
            tag="test_tag"
        )

        assert client.operator_code == "911"

    def test_create_client_with_operator_code(self):
        """Тестирует создание клиента с указанием кода оператора."""

        phone_number = "+7(999)456-78-90"
        operator_code = "999"
        client = Client.objects.create(
            phone_number=phone_number,
            operator_code=operator_code,
            tag="test_tag"
        )

        assert client.operator_code == "999"

    def test_calculate_operator_code(self):
        """Тестирует корректность работы метода calculate_operator_code."""

        phone_number = "+7(925)555-12-34"
        client = Client(phone_number=phone_number)

        assert client.calculate_operator_code() == "925"

    def test_filter_with_valid_data(self):
        """Тестирует работу метода filter с корректными данными."""

        client1 = Client.objects.create(
            phone_number="+7(925)111-22-33",
            operator_code="925",
            tag="tag1"
        )
        client2 = Client.objects.create(
            phone_number="+7(926)333-44-55",
            operator_code="926",
            tag="tag2"
        )

        clients = Client.filter(tag="tag1")

        assert clients.count() == 1
        assert clients.first().phone_number == "+7(925)111-22-33"
