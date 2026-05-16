"""Distribution API router (跨平台智能分发)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.schemas import (
    BestPublishTimeRequest,
    BestPublishTimeResponse,
    MessageResponse,
    PublishTaskCreate,
    PublishTaskOut,
)
from app.services.distribution_service import DistributionService

router = APIRouter(prefix="/distribution", tags=["内容分发 Distribution"])


@router.post("/schedule", response_model=PublishTaskOut, status_code=201)
async def schedule_publish(
    data: PublishTaskCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建定时发布任务."""
    svc = DistributionService(db)
    task = await svc.schedule_publish(current_user.id, data)
    return PublishTaskOut.model_validate(task)


@router.get("/tasks", response_model=list[PublishTaskOut])
async def list_publish_tasks(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取发布任务队列."""
    svc = DistributionService(db)
    tasks = await svc.list_tasks(current_user.id, page, page_size)
    return [PublishTaskOut.model_validate(t) for t in tasks]


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
async def cancel_publish_task(
    task_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """取消/暂停发布任务."""
    svc = DistributionService(db)
    await svc.cancel_task(task_id, current_user.id)
    return MessageResponse.ok("发布任务已取消")


@router.post("/best-time", response_model=BestPublishTimeResponse)
async def get_best_publish_time(
    data: BestPublishTimeRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """获取指定平台的最优发布时间建议."""
    svc = DistributionService(db)
    return await svc.get_best_publish_time(data)
