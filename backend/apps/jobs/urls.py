from django.urls import path

from apps.jobs.views import JobSearchAPIView


urlpatterns = [

    path(
        "search/",
        JobSearchAPIView.as_view(),
        name="job-search",
    ),

]
