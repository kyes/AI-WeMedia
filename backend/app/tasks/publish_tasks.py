"""Background tasks: publish scheduled content to social platforms."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.publish_tasks.process_due_publish_tasks")
def process_due_publish_tasks() -> dict:
    """Pick up tasks that are scheduled_at <= now and attempt to publish."""
    try:
        return asyncio.run(_async_process_publishes())
    except Exception:
        logger.exception("Publish processing failed")
        return {"error": "publish processing failed"}


async def _async_process_publishes() -> dict:
    from app.database import AsyncSessionLocal
    from app.models import PublishStatus, PublishTask
    from sqlalchemy import select

    processed = 0
    failed = 0
    now = datetime.now(timezone.utc)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(PublishTask).where(
                PublishTask.status == PublishStatus.SCHEDULED,
                PublishTask.scheduled_at <= now,
            )
        )
        tasks = list(result.scalars())

        for task in tasks:
            task.status = PublishStatus.PUBLISHING
            await db.flush()
            try:
                # Real implementation: call platform API adapter to post the content
                success = await _publish_to_platform(task)
                if success:
                    task.status = PublishStatus.PUBLISHED
                    task.published_at = datetime.now(timezone.utc)
                    processed += 1
                else:
                    task.status = PublishStatus.FAILED
                    task.error_message = "Platform publish failed"
                    failed += 1
            except Exception as exc:
                task.status = PublishStatus.FAILED
                task.error_message = str(exc)
                failed += 1
                logger.exception("Failed to publish task %s", task.id)

        await db.commit()
    return {"processed": processed, "failed": failed}


async def _publish_to_platform(task) -> bool:  # type: ignore[no-untyped-def]
    """
    Placeholder: call the real platform adapter.
    Each platform (Douyin, Xiaohongshu, WeChat, etc.) has its own API client.
    Returns True on success.
    """
    logger.info("Publishing content %s to %s via account %s", task.content_id, task.platform, task.account_id)
    # await platform_adapter(task.platform).publish(task)
    return True  # Simulated success


@celery_app.task(bind=True, name="app.tasks.publish_tasks.publish_single_task", max_retries=3)
def publish_single_task(self, task_id: str) -> dict:
    """Immediately publish a single task (called when user triggers manual publish)."""
    try:
        return asyncio.run(_async_publish_single(task_id))
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10) from exc


async def _async_publish_single(task_id: str) -> dict:
    from app.database import AsyncSessionLocal
    from app.models import PublishStatus, PublishTask
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(PublishTask).where(PublishTask.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return {"error": "task not found"}
        task.status = PublishStatus.PUBLISHING
        await db.flush()
        success = await _publish_to_platform(task)
        task.status = PublishStatus.PUBLISHED if success else PublishStatus.FAILED
        if success:
            task.published_at = datetime.now(timezone.utc)
        await db.commit()
        return {"task_id": task_id, "status": task.status.value}
