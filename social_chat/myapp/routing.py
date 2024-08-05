from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:interest_id>/', consumers.ChatConsumer.as_asgi()),
    # path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),  # New route for notifications
]
