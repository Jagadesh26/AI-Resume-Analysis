# import os
# import django
# from celery import Celery
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

# app = Celery('config')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# # Explicitly import the compatibility task so the legacy scheduler name
# # is registered in the worker registry on startup.
# from apps.jobs.tasks import collect_jobs_task  # noqa: F401