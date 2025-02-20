from django.urls import path, include
from rest_framework.routers import SimpleRouter

from campaigns.views import MailingViewSet

campaign_router = SimpleRouter()

campaign_router.register(r'', MailingViewSet, basename='campaign')

urlpatterns = [
    path('api/', include(campaign_router.urls)),
]
