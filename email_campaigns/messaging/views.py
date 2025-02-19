from rest_framework.viewsets import ModelViewSet

from messaging.models import Client
from messaging.serializer import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer()
