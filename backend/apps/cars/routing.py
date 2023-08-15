from django.urls import path

from apps.chat.consumers import ChatConsumer

from .consumers import CarConsumer

websocket_urlpatterns = [
    path('', CarConsumer.as_asgi())
]