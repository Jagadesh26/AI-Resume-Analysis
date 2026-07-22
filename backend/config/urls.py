
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/auth/",
        include("apps.authentication.urls"),
    ),

    path(
        "api/v1/resumes/",
        include("apps.resumes.urls"),
    ),

    path(
        "api/v1/jobs/",
        include("apps.jobs.urls"),
    ),

    path(
        "api/v1/interview/",
        include("apps.interview.urls"),
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
