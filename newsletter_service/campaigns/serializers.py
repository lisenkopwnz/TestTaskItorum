from rest_framework import serializers

from campaigns.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'start_time', 'end_time', 'message_text', 'operator_code_filter', 'tag_filter']