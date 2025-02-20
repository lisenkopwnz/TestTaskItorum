from rest_framework.viewsets import ModelViewSet

from client.models import Client
from client.serializer import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer()
