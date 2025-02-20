from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from message.models import Message
from message.serializer import MessageSerializer


class MessageViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для модели Message с доступом только для чтения.

    Обрабатывает запросы GET для получения списка сообщений и их данных,
    используя сериализатор MessageSerializer.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
