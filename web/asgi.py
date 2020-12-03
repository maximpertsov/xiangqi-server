import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import xiangqi.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings.local")

application = get_asgi_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings.local")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(xiangqi.routing.websocket_urlpatterns),
    }
)
