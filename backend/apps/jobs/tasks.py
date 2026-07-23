# import logging

# from celery import shared_task

# logger = logging.getLogger(__name__)


# @shared_task(name="apps.scheduler.tasks.collect_jobs_task")
# def collect_jobs_task():
#     """
#     Compatibility task used by existing Celery schedules.

#     This keeps the worker from rejecting queued messages for the legacy
#     scheduler task name while the project continues to use the jobs app
#     for task discovery.
#     """
#     logger.info("collect_jobs_task executed")
#     return {"status": "ok", "message": "collect_jobs_task completed"}
