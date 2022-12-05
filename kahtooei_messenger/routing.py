from django.urls import re_path
from .consumers import ChatConsumer,ChatRoomConsumer


websocket_urlpatterns = [
    # re_path(r'ws/disposableConnect',ChatConsumer.as_asgi()),
    re_path(r"ws/messenger/(?P<token>\w+)/$",ChatRoomConsumer.as_asgi()),
    # re_path(r"ws/disposableConnect/",ChatRoomConsumer.as_asgi()),
]