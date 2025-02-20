from rest_framework.viewsets import ModelViewSet

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


class MailingViewSet(ModelViewSet):
    """
    ViewSet для управления маркетинговыми кампаниями.

    Поддерживает:
    - Получение списка рассылок (GET campaign/api/)
    - Получение конкретной рассылки (GET campaign/api/{id}/)
    - Создание рассылки (POST campaign/api/)
    - Обновление рассылки (PUT campaign/api/{id}/)
    - Частичное обновление рассылки (PATCH campaign/api/{id}/)
    - Удаление рассылки (DELETE campaign/api/{id}/)
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

