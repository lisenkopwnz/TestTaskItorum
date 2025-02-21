from rest_framework import serializers

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer
from client.models import Client
from client.serializer import ClientSerializer
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Message, включающий детали кампании и клиента.

    Для запросов GET предоставляет вложенные данные о связанной кампании
    и клиенте, включая их сериализованные представления.
    """
    campaign_details = CampaignSerializer(source='campaign', read_only=True)
    client_details = ClientSerializer(source='client', read_only=True)

    class Meta:
        """
        Метаинформация для сериализатора Message.

        Указывает поля, которые будут включены в сериализованный вывод.
        """
        model = Message
        fields = ['id', 'send_time', 'campaign', 'client']
