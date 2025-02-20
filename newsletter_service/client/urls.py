from django.urls import include, path
from rest_framework.routers import SimpleRouter

from client.views import ClientViewSet

client_router = SimpleRouter()

client_router.register(r'', ClientViewSet, basename='client')

urlpatterns = [
    path('api/', include(client_router.urls)),
]
