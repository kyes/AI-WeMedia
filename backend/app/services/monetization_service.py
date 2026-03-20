"""Monetization service."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models import CommercialOrder, OrderStatus, RevenueRecord
from app.schemas import CommercialOrderCreate, CommercialOrderUpdate, RevenueSummary


class MonetizationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_orders(
        self,
        user_id: str,
        status: OrderStatus | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[CommercialOrder], int]:
        query = select(CommercialOrder).where(CommercialOrder.owner_id == user_id)
        if status:
            query = query.where(CommercialOrder.status == status)
        total = (await self.db.execute(
            select(func.count()).select_from(query.subquery())
        )).scalar_one()
        query = query.order_by(CommercialOrder.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        results = await self.db.execute(query)
        return list(results.scalars()), total

    async def create_order(self, user_id: str, data: CommercialOrderCreate) -> CommercialOrder:
        order = CommercialOrder(
            owner_id=user_id,
            account_id=data.account_id,
            brand_name=data.brand_name,
            order_type=data.order_type,
            amount=data.amount,
            commission_rate=data.commission_rate,
            platform=data.platform,
            requirements=data.requirements,
            deadline=data.deadline,
        )
        self.db.add(order)
        await self.db.flush()
        return order

    async def update_order(
        self, order_id: str, user_id: str, data: CommercialOrderUpdate
    ) -> CommercialOrder:
        result = await self.db.execute(
            select(CommercialOrder).where(
                CommercialOrder.id == order_id, CommercialOrder.owner_id == user_id
            )
        )
        order = result.scalar_one_or_none()
        if not order:
            raise NotFoundError("Order not found")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(order, field, value)
        await self.db.flush()
        return order

    async def get_revenue_summary(self, user_id: str) -> RevenueSummary:
        since = datetime.now(timezone.utc) - timedelta(days=30)
        result = await self.db.execute(
            select(RevenueRecord).where(
                RevenueRecord.owner_id == user_id,
                RevenueRecord.earned_at >= since,
            )
        )
        records = list(result.scalars())

        total = sum(r.amount for r in records)
        by_channel: dict[str, float] = {}
        for r in records:
            by_channel[r.channel] = by_channel.get(r.channel, 0) + r.amount

        # Monthly trend (last 5 months)
        monthly: dict[str, float] = {}
        for r in records:
            key = r.earned_at.strftime("%Y-%m")
            monthly[key] = monthly.get(key, 0) + r.amount

        return RevenueSummary(
            total=total,
            by_channel=by_channel,
            monthly_trend=[
                {"month": k, "total": v} for k, v in sorted(monthly.items())
            ],
        )

    async def record_revenue(
        self,
        user_id: str,
        channel: str,
        amount: float,
        description: str | None = None,
        reference_id: str | None = None,
        account_id: str | None = None,
    ) -> RevenueRecord:
        record = RevenueRecord(
            owner_id=user_id,
            account_id=account_id,
            channel=channel,
            amount=amount,
            description=description,
            reference_id=reference_id,
        )
        self.db.add(record)
        await self.db.flush()
        return record
