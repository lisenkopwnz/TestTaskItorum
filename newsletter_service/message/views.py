from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from message.models import Client, Campaign, Message
from message.serializer import ClientSerializer, CampaignSerializer, MessageSerializer





class MailingViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

class MessageViewSet(ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer