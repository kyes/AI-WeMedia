"""Interaction & fan profile router (用户画像与精准互动)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import FanProfile, InteractionTask
from app.schemas import (
    FanProfileOut,
    InteractionTaskCreate,
    InteractionTaskOut,
    MessageResponse,
    PaginatedResponse,
)

router = APIRouter(prefix="/interaction", tags=["用户互动 Interaction"])


@router.get("/fans", response_model=PaginatedResponse)
async def list_fans(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    account_id: str | None = Query(None),
    segment: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取粉丝画像列表."""
    from sqlalchemy import func
    from app.models import SocialAccount
    query = select(FanProfile).join(
        SocialAccount, FanProfile.account_id == SocialAccount.id
    ).where(SocialAccount.owner_id == current_user.id)
    if account_id:
        query = query.where(FanProfile.account_id == account_id)
    if segment:
        query = query.where(FanProfile.segment == segment)
    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
    fans = (await db.execute(query.offset((page - 1) * page_size).limit(page_size))).scalars()
    return PaginatedResponse(
        items=[FanProfileOut.model_validate(f) for f in fans],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/tasks", response_model=list[InteractionTaskOut])
async def list_tasks(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取自动化互动任务列表."""
    result = await db.execute(
        select(InteractionTask).where(InteractionTask.owner_id == current_user.id)
    )
    return [InteractionTaskOut.model_validate(t) for t in result.scalars()]


@router.post("/tasks", response_model=InteractionTaskOut, status_code=201)
async def create_task(
    data: InteractionTaskCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建自动化互动任务规则."""
    task = InteractionTask(
        owner_id=current_user.id,
        account_id=data.account_id,
        name=data.name,
        trigger_type=data.trigger_type,
        trigger_config=data.trigger_config,
        action_type=data.action_type,
        message_template=data.message_template,
        target_segment=data.target_segment,
    )
    db.add(task)
    await db.flush()
    return InteractionTaskOut.model_validate(task)


@router.patch("/tasks/{task_id}/toggle", response_model=InteractionTaskOut)
async def toggle_task(
    task_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """开启/关闭互动任务."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(InteractionTask).where(
            InteractionTask.id == task_id, InteractionTask.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task not found")
    task.is_active = not task.is_active
    await db.flush()
    return InteractionTaskOut.model_validate(task)


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    task_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(InteractionTask).where(
            InteractionTask.id == task_id, InteractionTask.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    if not task:
        raise NotFoundError("Task not found")
    await db.delete(task)
    return MessageResponse.ok("互动任务已删除")
