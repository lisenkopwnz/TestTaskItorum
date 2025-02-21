import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from campaigns.models import Campaign


# Фикстура для создания данных рассылки
@pytest.fixture
def campaign_data():
    """Фикстура для создания данных рассылки."""
    return {
        'start_time': timezone.now(),
        'end_time': timezone.now() + timezone.timedelta(days=1),
        'message_text': "Test message",
        'operator_code_filter': "123",
        'tag_filter': "test_tag"
    }

# Фикстура для создания самой рассылки в базе данных
@pytest.fixture
def campaign(campaign_data):
    """Фикстура для создания самой рассылки в базе данных."""
    return Campaign.objects.create(**campaign_data)

@pytest.mark.django_db
def test_campaign_str(campaign):
    """Тестирует метод __str__ для правильного вывода строки."""
    expected_str = f"Рассылка ID-{campaign.pk} - {campaign.start_time} до {campaign.end_time}"
    assert str(campaign) == expected_str

@pytest.mark.django_db
def test_campaign_clean_end_time_in_past(campaign_data):
    """Тестирует, что ошибка выбрасывается, если дата окончания раньше даты начала."""
    campaign_data['end_time'] = timezone.now() - timezone.timedelta(days=1)
    campaign = Campaign(**campaign_data)

    with pytest.raises(ValidationError) as exc_info:
        campaign.clean()

    assert "Дата окончания не может быть раньше даты начала." in str(exc_info.value)

@pytest.mark.django_db
def test_campaign_clean_end_time_in_past(campaign_data):
    """Тестирует, что ошибка выбрасывается, если дата окончания в прошлом."""
    campaign_data['end_time'] = timezone.now() - timezone.timedelta(days=1)
    campaign = Campaign(**campaign_data)

    with pytest.raises(ValidationError) as exc_info:
        campaign.clean()

    assert "Дата окончания не может быть раньше даты начала." in str(exc_info.value)

@pytest.mark.django_db
def test_campaign_clean_end_time_before_start_time(campaign_data):
    """Тестирует, что ошибка выбрасывается, если дата окончания раньше даты начала."""
    campaign_data['start_time'] = timezone.now() + timezone.timedelta(days=1)
    campaign_data['end_time'] = timezone.now()
    campaign = Campaign(**campaign_data)

    with pytest.raises(ValidationError, match="Дата окончания не может быть раньше даты начала."):
        campaign.clean()

@pytest.mark.django_db
def test_campaign_get_success(campaign):
    """Тестирует успешное извлечение рассылки с помощью метода get."""
    retrieved_campaign = Campaign.get(id=campaign.id)
    assert retrieved_campaign == campaign

@pytest.mark.django_db
def test_campaign_get_not_found():
    """Тестирует поведение метода get, когда рассылка не найдена."""
    with pytest.raises(ValidationError, match="Рассылка не найдена."):
        Campaign.get(id=999)
