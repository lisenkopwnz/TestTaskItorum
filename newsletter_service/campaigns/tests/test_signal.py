import pytest
from unittest.mock import patch
from django.utils.timezone import now, timedelta
from campaigns.models import Campaign




@pytest.mark.django_db
class TestScheduleMailingSignal:

    @patch('campaigns.signals.send_mailing.delay')
    @patch('campaigns.signals.send_mailing.apply_async')
    def test_signal_triggered_immediate_mailing(self, mock_apply_async, mock_delay):
        """Тестирует, что сигнал вызывает немедленный запуск задачи, если время старта уже наступило."""

        campaign = Campaign.objects.create(
            start_time=now() - timedelta(days=1),  # время старта в прошлом
            end_time=now() + timedelta(days=1),
            message_text="Test message",
            operator_code_filter="123",
            tag_filter="test_tag"
        )

        mock_delay.assert_called_once_with(campaign.id)
        mock_apply_async.assert_not_called()

    @patch('campaigns.signals.send_mailing.delay')
    @patch('campaigns.signals.send_mailing.apply_async')
    def test_signal_triggered_scheduled_mailing(self, mock_apply_async, mock_delay):
        """Тестирует, что сигнал вызывает отложенный запуск задачи, если время старта в будущем."""

        campaign = Campaign.objects.create(
            start_time=now() + timedelta(days=1),
            end_time=now() + timedelta(days=2),
            message_text="Test message",
            operator_code_filter="123",
            tag_filter="test_tag"
        )

        mock_apply_async.assert_called_once_with((campaign.id,), eta=campaign.start_time)
        mock_delay.assert_not_called()
