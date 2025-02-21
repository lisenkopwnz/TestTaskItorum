from datetime import datetime
from django.utils.timezone import timezone
from unittest.mock import patch, MagicMock
from ..task import send_mailing
from campaigns.models import Campaign
from client.models import Client
from message.models import Message
from django.test import TestCase

class TestSendMailingTask(TestCase):
    @patch('campaigns.task.Campaign.get')  # Мокаем Campaign.get для получения кампании
    @patch('campaigns.task.Client.filter')  # Мокаем фильтрацию клиентов
    @patch('campaigns.task.Message.objects.create')  # Мокаем создание сообщений
    def test_send_mailing_task(self, mock_message_create, mock_client_filter, mock_campaign_get):
        # Мокаем кампанию
        mock_campaign = MagicMock(spec=Campaign)
        mock_campaign.id = 1
        mock_campaign.start_time = datetime(2025, 2, 21, 0, 0, 0, tzinfo=timezone.utc)
        mock_campaign.end_time = datetime(2025, 2, 22, 0, 0, 0, tzinfo=timezone.utc)
        mock_campaign.operator_code_filter = 'operator_code'
        mock_campaign.tag_filter = 'tag'
        mock_campaign.message_text = 'Test message'

        mock_campaign_get.return_value = mock_campaign

        # Мокаем клиента
        mock_client = MagicMock(spec=Client)
        mock_client.phone_number = '+79111234567'
        mock_client_filter.return_value = [mock_client]  # Возвращаем список клиентов

        # Мокаем создание сообщения
        mock_message_create.return_value = MagicMock(spec=Message)

        # Запуск задачи
        send_mailing.apply(args=[1])

        mock_client_filter.assert_called_once_with(operator_code=mock_campaign.operator_code_filter,
                                                   tag=mock_campaign.tag_filter)
