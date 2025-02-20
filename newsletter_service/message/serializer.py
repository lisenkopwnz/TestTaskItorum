from rest_framework import serializers

from client.serializer import ClientSerializer
from message.models import Campaign, Message

class MessageSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = ['id', 'send_time', 'campaign', 'client']
