from django.urls import path

from apps.interview.websocket.consumers import InterviewConsumer



websocket_urlpatterns = [
    path(
        "ws/interview/<uuid:conversation_id>/",
        InterviewConsumer.as_asgi(),
    ),
]