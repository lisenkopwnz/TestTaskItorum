from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from message.models import Message
from message.serializer import MessageSerializer


class MessageViewSet(ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
