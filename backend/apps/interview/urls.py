
from django.urls import path, include
from .views import *


urlpatterns = [
    path("upload/", InterviewUploadAPIView.as_view(), name="interview-upload"),
    path("report/<uuid:session_id>/", InterviewReportAPIView.as_view(), name="interview-report"),
    path("history/", InterviewHistoryAPIView.as_view(), name="interview-history"),
    path("<uuid:session_id>/", InterviewDetailAPIView.as_view(), name="interview-detail"),
]
