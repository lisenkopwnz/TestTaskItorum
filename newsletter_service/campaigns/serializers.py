from rest_framework import serializers

from campaigns.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Campaign.

    Используется для преобразования данных кампании в JSON и обратно.

    Поля:
        start_time (DateTimeField): Дата и время начала кампании.
        end_time (DateTimeField): Дата и время окончания кампании.
        message_text (TextField): Текст сообщения, которое будет отправлено клиентам.
        operator_code_filter (CharField): Код оператора (необязательное поле).
        tag_filter (CharField): Тег для фильтрации получателей.

    Класс Meta:
        model (Campaign): Указывает, что сериализатор работает с моделью Campaign.
        fields (list): Определяет, какие поля включены в сериализацию.
    """

    class Meta:
        model = Campaign
        fields = ['id','start_time', 'end_time', 'message_text', 'operator_code_filter', 'tag_filter']
