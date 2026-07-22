import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

from apps.interview.websocket.routing import websocket_urlpatterns

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(

    {

        "http": django_asgi_app,

        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),

    }

)
