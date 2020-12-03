from django.urls import re_path

from xiangqi import consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<slug>\w+)$", consumers.EventConsumer.as_asgi())
]
