from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import xiangqi.routing

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(
            URLRouter(xiangqi.routing.websocket_urlpatterns)
        )
    }
)
