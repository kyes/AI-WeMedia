"""Content API router (多模态内容生成)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import ContentStatus, PlatformType
from app.schemas import (
    ContentAdaptRequest,
    ContentCreate,
    ContentGenerateRequest,
    ContentOut,
    ContentUpdate,
    MessageResponse,
    PaginatedResponse,
)
from app.services.content_service import ContentService

router = APIRouter(prefix="/contents", tags=["内容生成 Content"])


@router.get("", response_model=PaginatedResponse)
async def list_contents(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    status: ContentStatus | None = Query(None),
    platform: PlatformType | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取内容列表."""
    svc = ContentService(db)
    items, total = await svc.list_contents(current_user.id, status, platform, page, page_size)
    return PaginatedResponse(
        items=[ContentOut.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ContentOut, status_code=201)
async def create_content(
    data: ContentCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """手动创建内容草稿."""
    svc = ContentService(db)
    return await svc.create_content(current_user.id, data)


@router.post("/generate", response_model=ContentOut, status_code=201)
async def generate_content(
    data: ContentGenerateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """AI 一键生成内容（含合规检测）."""
    svc = ContentService(db)
    return await svc.generate_ai_content(current_user.id, data)


@router.post("/adapt", response_model=ContentOut)
async def adapt_content(
    data: ContentAdaptRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """将内容适配到多个平台版本."""
    svc = ContentService(db)
    return await svc.adapt_to_platforms(current_user.id, data)


@router.get("/{content_id}", response_model=ContentOut)
async def get_content(
    content_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = ContentService(db)
    return await svc.get_content(content_id, current_user.id)


@router.put("/{content_id}", response_model=ContentOut)
async def update_content(
    content_id: str,
    data: ContentUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """编辑内容."""
    svc = ContentService(db)
    return await svc.update_content(content_id, current_user.id, data)


@router.delete("/{content_id}", response_model=MessageResponse)
async def delete_content(
    content_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    svc = ContentService(db)
    await svc.delete_content(content_id, current_user.id)
    return MessageResponse.ok("内容已删除")
