from rest_framework import serializers

from messaging.models import Client, Campaign, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'operator_code', 'tag']

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
