"""Background tasks: AI content generation (CPU-heavy, async-safe via Celery)."""
from __future__ import annotations

import asyncio
import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.content_tasks.generate_ai_content_task", max_retries=3)
def generate_ai_content_task(self, content_id: str, user_id: str) -> dict:
    """
    Run AI content generation for a content record in the background.
    The actual heavy lifting uses an event-loop inside the Celery worker.
    """
    try:
        result = asyncio.run(_async_generate_content(content_id, user_id))
        return {"status": "success", "content_id": content_id, **result}
    except Exception as exc:
        logger.exception("Content generation failed for %s", content_id)
        raise self.retry(exc=exc, countdown=30) from exc


async def _async_generate_content(content_id: str, user_id: str) -> dict:
    from app.database import AsyncSessionLocal
    from app.services.ai_service import AIService
    from sqlalchemy import select
    from app.models import Content

    ai = AIService()
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Content).where(Content.id == content_id))
        content = result.scalar_one_or_none()
        if not content:
            return {"error": "content not found"}

        platform = content.platform.value if content.platform else "xiaohongshu"
        raw = await ai.generate_content(
            topic=content.title,
            platform=platform,
            style=content.style or "专业干货",
        )
        compliance = await ai.check_compliance(raw.get("raw", ""))

        content.body = raw.get("raw", "")
        content.ai_provider = raw.get("ai_provider")
        content.originality_score = compliance.get("originality")
        content.readability_score = compliance.get("readability")
        content.compliance_score = compliance.get("compliance")
        content.value_score = compliance.get("value")
        await db.commit()
        return {"tokens_used": raw.get("tokens_used", 0)}


@celery_app.task(name="app.tasks.content_tasks.check_content_compliance_task")
def check_content_compliance_task(content_id: str) -> dict:
    """Re-run compliance check for a content piece."""
    try:
        return asyncio.run(_async_check_compliance(content_id))
    except Exception:
        logger.exception("Compliance check failed for %s", content_id)
        return {"error": "compliance check failed"}


async def _async_check_compliance(content_id: str) -> dict:
    from app.database import AsyncSessionLocal
    from app.services.ai_service import AIService
    from sqlalchemy import select
    from app.models import Content

    ai = AIService()
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Content).where(Content.id == content_id))
        content = result.scalar_one_or_none()
        if not content or not content.body:
            return {}
        scores = await ai.check_compliance(content.body)
        content.originality_score = scores.get("originality")
        content.readability_score = scores.get("readability")
        content.compliance_score = scores.get("compliance")
        content.value_score = scores.get("value")
        await db.commit()
        return scores
