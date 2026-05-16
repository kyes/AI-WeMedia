"""Analytics API router (数据检测与智能决策)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.schemas import (
    AccountAnalyticsOut,
    AlertRuleCreate,
    AlertRuleOut,
    DashboardSummary,
    MessageResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["数据分析 Analytics"])


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取数据概览仪表盘（多平台聚合）."""
    svc = AnalyticsService(db)
    return await svc.get_dashboard(current_user.id)


@router.get("/accounts/{account_id}", response_model=list[AccountAnalyticsOut])
async def get_account_analytics(
    account_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    days: int = Query(7, ge=1, le=365),
):
    """获取指定账号的历史数据."""
    svc = AnalyticsService(db)
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    items = await svc.get_account_analytics(account_id, start, end)
    return [AccountAnalyticsOut.model_validate(i) for i in items]


@router.get("/alerts", response_model=list[AlertRuleOut])
async def list_alert_rules(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取所有预警规则."""
    from sqlalchemy import select
    from app.models import AlertRule
    result = await db.execute(select(AlertRule).where(AlertRule.owner_id == current_user.id))
    return [AlertRuleOut.model_validate(r) for r in result.scalars()]


@router.post("/alerts", response_model=AlertRuleOut, status_code=201)
async def create_alert_rule(
    data: AlertRuleCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建数据预警规则."""
    svc = AnalyticsService(db)
    rule = await svc.create_alert_rule(current_user.id, data)
    return AlertRuleOut.model_validate(rule)


@router.delete("/alerts/{rule_id}", response_model=MessageResponse)
async def delete_alert_rule(
    rule_id: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """删除预警规则."""
    from sqlalchemy import select
    from app.models import AlertRule
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(AlertRule).where(AlertRule.id == rule_id, AlertRule.owner_id == current_user.id)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("Alert rule not found")
    await db.delete(rule)
    return MessageResponse.ok("预警规则已删除")
