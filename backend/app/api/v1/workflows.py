"""Workflow automation router (自动化工作流)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import WorkflowRule
from app.schemas import MessageResponse, WorkflowRuleCreate, WorkflowRuleOut

router = APIRouter(prefix="/workflows", tags=["自动化工作流 Workflows"])


@router.get("", response_model=list[WorkflowRuleOut])
async def list_workflows(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取自动化工作流规则列表."""
    result = await db.execute(
        select(WorkflowRule).where(WorkflowRule.owner_id == current_user.id).order_by(WorkflowRule.created_at.desc())
    )
    return [WorkflowRuleOut.model_validate(r) for r in result.scalars()]


@router.post("", response_model=WorkflowRuleOut, status_code=201)
async def create_workflow(
    data: WorkflowRuleCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建自动化工作流规则."""
    rule = WorkflowRule(
        owner_id=current_user.id,
        name=data.name,
        description=data.description,
        trigger_type=data.trigger_type,
        trigger_config=data.trigger_config,
        action_type=data.action_type,
        action_config=data.action_config,
    )
    db.add(rule)
    await db.flush()
    return WorkflowRuleOut.model_validate(rule)


@router.patch("/{rule_id}/toggle", response_model=WorkflowRuleOut)
async def toggle_workflow(
    rule_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """开启/关闭工作流规则."""
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(WorkflowRule).where(WorkflowRule.id == rule_id, WorkflowRule.owner_id == current_user.id)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("Workflow not found")
    rule.is_active = not rule.is_active
    await db.flush()
    return WorkflowRuleOut.model_validate(rule)


@router.delete("/{rule_id}", response_model=MessageResponse)
async def delete_workflow(
    rule_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(WorkflowRule).where(WorkflowRule.id == rule_id, WorkflowRule.owner_id == current_user.id)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("Workflow not found")
    await db.delete(rule)
    return MessageResponse.ok("工作流已删除")
