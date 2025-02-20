from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from campaigns.views import MailingViewSet

message_router = SimpleRouter()

message_router.register(r'', MailingViewSet, basename='message')


urlpatterns = [
    path('api/', include(message_router.urls)),
]