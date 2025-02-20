from rest_framework.viewsets import ModelViewSet

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class MailingViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

