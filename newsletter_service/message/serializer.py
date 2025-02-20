from rest_framework import serializers

from client.serializer import ClientSerializer
from message.models import Campaign, Message


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'start_time', 'end_time', 'message_text', 'operator_code_filter', 'tag_filter']

class MessageSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = ['id', 'send_time', 'campaign', 'client']
