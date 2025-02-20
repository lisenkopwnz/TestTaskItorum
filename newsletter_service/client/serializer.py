from rest_framework import serializers

from client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Client.

    Преобразует данные клиента в формат JSON и обратно.
    Поле `operator_code` доступно только для чтения, так как оно вычисляется автоматически.

    Атрибуты:
        phone_number (PhoneNumberField): Номер телефона клиента в формате E.164.
        operator_code (CharField): Код оператора, доступен только для чтения.
        tag (CharField): Тег клиента, используемый для фильтрации.
    """

    operator_code = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = ['phone_number', 'operator_code', 'tag']
