# from django.urls import path
# from . import consumers

# websocket_urlpatterns = [
#     path('ws/chat/<int:interest_id>/', consumers.ChatConsumer.as_asgi()),
#     # path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),  # New route for notifications
# ]
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<interest_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]