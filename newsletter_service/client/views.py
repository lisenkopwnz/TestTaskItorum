from rest_framework.viewsets import ModelViewSet

from client.models import Client
from client.serializer import ClientSerializer


class ClientViewSet(ModelViewSet):
    """
    ViewSet для управления данными клиентов.

    Поддерживает следующие действия:
    - Получение списка клиентов (GET client/api/)
    - Получение данных конкретного клиента (GET client/api/{id}/)
    - Создание нового клиента (POST client/client/api/)
    - Обновление данных клиента (PUT client/api/{id}/)
    - Частичное обновление данных клиента (PATCH client/api/{id}/)
    - Удаление клиента (DELETE client/api/{id}/)

    Атрибуты:
        queryset (QuerySet): Все объекты клиентов из базы данных.
        serializer_class (ClientSerializer): Сериализатор, используемый для преобразования данных модели Client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
