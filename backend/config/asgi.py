# import os

# from channels.routing import ProtocolTypeRouter
# from channels.routing import URLRouter
# from channels.auth import AuthMiddlewareStack

# from django.core.asgi import get_asgi_application

# from apps.interview.websocket.routing import websocket_urlpatterns

# os.environ.setdefault(
#     "DJANGO_SETTINGS_MODULE",
#     "config.settings",
# )

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(

#     {

#         "http": django_asgi_app,

#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),

#     }

# )





import os

from django.core.asgi import get_asgi_application

# 1. Set environment variable first
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

# 2. Initialize Django ASGI application early to populate app registry
django_asgi_app = get_asgi_application()

# 3. Import Channels components & routing AFTER get_asgi_application()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.interview.websocket.routing import websocket_urlpatterns

# 4. Define ASGI application router
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