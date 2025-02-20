from django.urls import include, path
from rest_framework.routers import DefaultRouter

from client.views import ClientViewSet

client_router = DefaultRouter()

client_router.register(r'client', ClientViewSet, basename='client')

urlpatterns = [
    path('api/', include(client_router.urls)),
]