"""Celery application factory."""
from __future__ import annotations

from celery import Celery

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "wemedia",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.content_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.publish_tasks",
        "app.tasks.notification_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        # Sync platform analytics every hour
        "sync-platform-analytics": {
            "task": "app.tasks.analytics_tasks.sync_all_platform_analytics",
            "schedule": 3600.0,
        },
        # Check alert rules every 15 minutes
        "check-alert-rules": {
            "task": "app.tasks.analytics_tasks.check_alert_rules",
            "schedule": 900.0,
        },
        # Process scheduled publish tasks every minute
        "process-scheduled-publishes": {
            "task": "app.tasks.publish_tasks.process_due_publish_tasks",
            "schedule": 60.0,
        },
    },
)
