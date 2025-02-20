from rest_framework import serializers

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer
from client.models import Client
from client.serializer import ClientSerializer
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Для записи (POST, PUT, PATCH) – передаём только ID
    campaign = serializers.PrimaryKeyRelatedField(queryset=Campaign.objects.all(), write_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)

    # Для чтения (GET) – получаем вложенные объекты
    campaign_details = CampaignSerializer(source='campaign', read_only=True)
    client_details = ClientSerializer(source='client', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'send_time', 'campaign', 'client']
