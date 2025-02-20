from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaigns.views import MailingViewSet

campaign_router = DefaultRouter()

campaign_router.register('campaign', MailingViewSet, basename='campaign')


urlpatterns = [
    path('api/', include(campaign_router.urls)),
]