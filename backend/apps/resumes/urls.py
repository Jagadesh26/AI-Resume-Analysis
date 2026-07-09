from django.urls import path

from apps.resumes.views import ResumeAnalyzeAPIView





urlpatterns = [

    path(
        "analyze/",
        ResumeAnalyzeAPIView.as_view(),
        name="resume-analyze",
    ),

]