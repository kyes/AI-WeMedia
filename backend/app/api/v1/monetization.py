"""Monetization API router (商业变现赋能)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import OrderStatus
from app.schemas import (
    CommercialOrderCreate,
    CommercialOrderOut,
    CommercialOrderUpdate,
    PaginatedResponse,
    RevenueSummary,
)
from app.services.monetization_service import MonetizationService

router = APIRouter(prefix="/monetization", tags=["商业变现 Monetization"])


@router.get("/revenue", response_model=RevenueSummary)
async def get_revenue_summary(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """获取变现收入汇总（30天）."""
    svc = MonetizationService(db)
    return await svc.get_revenue_summary(current_user.id)


@router.get("/orders", response_model=PaginatedResponse)
async def list_orders(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    status: OrderStatus | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """获取商单列表."""
    svc = MonetizationService(db)
    items, total = await svc.list_orders(current_user.id, status, page, page_size)
    return PaginatedResponse(
        items=[CommercialOrderOut.model_validate(o) for o in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.post("/orders", response_model=CommercialOrderOut, status_code=201)
async def create_order(
    data: CommercialOrderCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """创建商单."""
    svc = MonetizationService(db)
    order = await svc.create_order(current_user.id, data)
    return CommercialOrderOut.model_validate(order)


@router.put("/orders/{order_id}", response_model=CommercialOrderOut)
async def update_order(
    order_id: str,
    data: CommercialOrderUpdate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """更新商单状态/信息."""
    svc = MonetizationService(db)
    order = await svc.update_order(order_id, current_user.id, data)
    return CommercialOrderOut.model_validate(order)
