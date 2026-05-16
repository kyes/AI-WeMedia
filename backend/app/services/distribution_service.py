"""Distribution / publishing service."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models import Content, PublishStatus, PublishTask, SocialAccount
from app.schemas import BestPublishTimeRequest, BestPublishTimeResponse, PublishTaskCreate


# Heuristic best publish times per platform
_BEST_TIMES: dict[str, list[tuple[str, float]]] = {
    "douyin":       [("12:00", 85), ("20:00", 92), ("21:30", 78)],
    "xiaohongshu":  [("12:30", 72), ("21:00", 88), ("22:30", 80)],
    "wechat":       [("08:00", 65), ("20:30", 90)],
    "shipin":       [("12:00", 70), ("19:00", 85), ("21:00", 80)],
    "kuaishou":     [("12:00", 75), ("20:00", 88), ("21:00", 82)],
    "bilibili":     [("18:00", 78), ("20:00", 90), ("22:00", 72)],
}


class DistributionService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def schedule_publish(
        self, user_id: str, data: PublishTaskCreate
    ) -> PublishTask:
        """Create a scheduled publish task (Celery picks it up later)."""
        # Validate content & account belong to user
        content_res = await self.db.execute(
            select(Content).where(Content.id == data.content_id, Content.creator_id == user_id)
        )
        if not content_res.scalar_one_or_none():
            raise NotFoundError("Content not found")

        account_res = await self.db.execute(
            select(SocialAccount).where(
                SocialAccount.id == data.account_id,
                SocialAccount.owner_id == user_id,
            )
        )
        if not account_res.scalar_one_or_none():
            raise NotFoundError("Social account not found")

        task = PublishTask(
            content_id=data.content_id,
            account_id=data.account_id,
            platform=data.platform,
            scheduled_at=data.scheduled_at,
        )
        self.db.add(task)
        await self.db.flush()

        # In production, enqueue to Celery here:
        # publish_content_task.apply_async(args=[task.id], eta=data.scheduled_at)
        return task

    async def get_best_publish_time(
        self, data: BestPublishTimeRequest
    ) -> BestPublishTimeResponse:
        times_data = _BEST_TIMES.get(data.platform.value, [("12:00", 75), ("20:00", 85)])
        times = [t for t, _ in times_data]
        scores = [s for _, s in times_data]
        return BestPublishTimeResponse(
            platform=data.platform,
            recommended_times=times,
            heat_scores=scores,
        )

    async def list_tasks(
        self, user_id: str, page: int = 1, page_size: int = 20
    ) -> list[PublishTask]:
        from sqlalchemy import func
        result = await self.db.execute(
            select(PublishTask)
            .join(Content, PublishTask.content_id == Content.id)
            .where(Content.creator_id == user_id)
            .order_by(PublishTask.scheduled_at)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars())

    async def cancel_task(self, task_id: str, user_id: str) -> PublishTask:
        result = await self.db.execute(
            select(PublishTask)
            .join(Content, PublishTask.content_id == Content.id)
            .where(PublishTask.id == task_id, Content.creator_id == user_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError("Publish task not found")
        task.status = PublishStatus.PAUSED
        await self.db.flush()
        return task
