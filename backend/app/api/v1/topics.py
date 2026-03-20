"""Topics API router (智能选题引擎)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import TopicStatus
from app.schemas import (
    MessageResponse,
    PaginatedResponse,
    TopicCreate,
    TopicGenerateRequest,
    TopicOut,
)
from app.services.content_service import TopicService

router = APIRouter(prefix="/topics", tags=["选题引擎 Topics"])


@router.get("", response_model=PaginatedResponse)
async def list_topics(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    account_id: str | None = Query(None),
    status: TopicStatus | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取选题库列表."""
    svc = TopicService(db)
    items, total = await svc.list_topics(current_user.id, account_id, status, page, page_size)
    return PaginatedResponse(
        items=[TopicOut.model_validate(t) for t in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=TopicOut, status_code=201)
async def create_topic(
    data: TopicCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """手动创建选题."""
    svc = TopicService(db)
    return await svc.create_topic(current_user.id, data)


@router.post("/generate", response_model=list[TopicOut], status_code=201)
async def generate_topics(
    data: TopicGenerateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """使用 AI 批量生成选题推荐."""
    svc = TopicService(db)
    topics = await svc.generate_ai_topics(current_user.id, data)
    return [TopicOut.model_validate(t) for t in topics]


@router.get("/{topic_id}", response_model=TopicOut)
async def get_topic(
    topic_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """获取单个选题详情."""
    svc = TopicService(db)
    return await svc.get_topic(topic_id, current_user.id)


@router.patch("/{topic_id}/status", response_model=TopicOut)
async def update_topic_status(
    topic_id: str,
    status: TopicStatus,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """更新选题状态（确认/取消等）."""
    svc = TopicService(db)
    return await svc.update_status(topic_id, current_user.id, status)
