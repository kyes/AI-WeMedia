"""AI technology support router (AI技术支撑 & 提示词模板)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import PromptTemplate
from app.schemas import (
    AIGenerateRequest,
    AIGenerateResponse,
    MessageResponse,
    PromptTemplateCreate,
    PromptTemplateOut,
)
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI 技术支撑 AI Support"])


@router.post("/generate", response_model=AIGenerateResponse)
async def generate(data: AIGenerateRequest, current_user: CurrentUser):
    """直接调用 AI 生成接口（通用）."""
    svc = AIService()
    return await svc.generate(data)


@router.get("/prompts", response_model=list[PromptTemplateOut])
async def list_prompts(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    scene: str | None = Query(None),
):
    """获取提示词模板库."""
    query = select(PromptTemplate).where(
        (PromptTemplate.owner_id == current_user.id) | (PromptTemplate.is_public == True)  # noqa: E712
    )
    if scene:
        query = query.where(PromptTemplate.scene == scene)
    result = await db.execute(query.order_by(PromptTemplate.use_count.desc()))
    return [PromptTemplateOut.model_validate(t) for t in result.scalars()]


@router.post("/prompts", response_model=PromptTemplateOut, status_code=201)
async def create_prompt(
    data: PromptTemplateCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建自定义提示词模板."""
    template = PromptTemplate(
        owner_id=current_user.id,
        name=data.name,
        scene=data.scene,
        template=data.template,
        variables=data.variables,
        is_public=data.is_public,
    )
    db.add(template)
    await db.flush()
    return PromptTemplateOut.model_validate(template)


@router.delete("/prompts/{template_id}", response_model=MessageResponse)
async def delete_prompt(
    template_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(PromptTemplate).where(
            PromptTemplate.id == template_id, PromptTemplate.owner_id == current_user.id
        )
    )
    tmpl = result.scalar_one_or_none()
    if not tmpl:
        raise NotFoundError("Template not found")
    await db.delete(tmpl)
    return MessageResponse.ok("模板已删除")
