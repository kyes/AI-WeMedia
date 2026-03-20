"""Analytics data service: aggregation, alerts, dashboard."""
from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AccountAnalytics, AlertRule, Content, ContentAnalytics, SocialAccount
from app.schemas import AlertRuleCreate, DashboardSummary


class AnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_dashboard(self, user_id: str) -> DashboardSummary:
        """Build dashboard summary from DB + simulated data."""
        accounts_result = await self.db.execute(
            select(SocialAccount).where(SocialAccount.owner_id == user_id, SocialAccount.is_active == True)  # noqa: E712
        )
        accounts = list(accounts_result.scalars())

        total_followers = sum(a.followers_count for a in accounts)
        # Last 7 days aggregation
        since = datetime.now(timezone.utc) - timedelta(days=7)
        analytics_result = await self.db.execute(
            select(AccountAnalytics).where(
                AccountAnalytics.account_id.in_([a.id for a in accounts]),
                AccountAnalytics.date >= since,
            )
        )
        analytics = list(analytics_result.scalars())

        weekly_views = sum(a.views for a in analytics)
        weekly_interactions = sum(a.likes + a.comments + a.shares for a in analytics)
        monthly_revenue = sum(a.revenue for a in analytics)

        # Build growth trend (simulate if no real data)
        growth_trend = self._build_trend(analytics, accounts)

        # Platform breakdown
        platform_breakdown = [
            {
                "platform": a.platform.value,
                "name": a.name,
                "followers": a.followers_count,
                "health_score": a.health_score or 75.0,
            }
            for a in accounts
        ]

        # Top content
        top_content_result = await self.db.execute(
            select(Content, func.sum(ContentAnalytics.views).label("total_views"))
            .join(ContentAnalytics, Content.id == ContentAnalytics.content_id, isouter=True)
            .where(Content.creator_id == user_id)
            .group_by(Content.id)
            .order_by(func.sum(ContentAnalytics.views).desc().nullslast())
            .limit(5)
        )
        top_content = [
            {
                "id": row.Content.id,
                "title": row.Content.title,
                "platform": row.Content.platform.value if row.Content.platform else None,
                "views": row.total_views or 0,
            }
            for row in top_content_result
        ]

        # Alerts
        alerts = await self._get_active_alerts(user_id)

        avg_health = (
            sum(a.health_score or 75 for a in accounts) / len(accounts) if accounts else 75.0
        )

        return DashboardSummary(
            total_followers=total_followers,
            weekly_views=weekly_views,
            weekly_interactions=weekly_interactions,
            monthly_revenue=monthly_revenue,
            health_score=round(avg_health, 1),
            platform_breakdown=platform_breakdown,
            growth_trend=growth_trend,
            top_content=top_content,
            alerts=alerts,
        )

    def _build_trend(
        self, analytics: list[AccountAnalytics], accounts: list[SocialAccount]
    ) -> list[dict]:
        """Build 7-day trend; if no DB data, return simulated data."""
        if analytics:
            by_date: dict[str, dict] = {}
            for a in analytics:
                key = a.date.strftime("%m/%d")
                row = by_date.setdefault(key, {"date": key, "followers": 0, "views": 0, "interactions": 0})
                row["followers"] += a.followers
                row["views"] += a.views
                row["interactions"] += a.likes + a.comments + a.shares
            return sorted(by_date.values(), key=lambda x: x["date"])
        # Simulated
        base_followers = sum(a.followers_count for a in accounts) or 50000
        trend = []
        for i in range(7):
            date = datetime.now(timezone.utc) - timedelta(days=6 - i)
            trend.append({
                "date": date.strftime("%m/%d"),
                "followers": base_followers - 1500 + i * 200 + random.randint(-100, 100),
                "views": random.randint(100000, 250000),
                "interactions": random.randint(5000, 15000),
            })
        return trend

    async def _get_active_alerts(self, user_id: str) -> list[dict]:
        result = await self.db.execute(
            select(AlertRule).where(AlertRule.owner_id == user_id, AlertRule.is_active == True)  # noqa: E712
        )
        rules = list(result.scalars())
        return [
            {
                "id": r.id,
                "name": r.name,
                "metric": r.metric,
                "threshold": r.threshold,
                "last_triggered_at": r.last_triggered_at.isoformat() if r.last_triggered_at else None,
            }
            for r in rules
        ]

    async def get_account_analytics(
        self,
        account_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> list[AccountAnalytics]:
        result = await self.db.execute(
            select(AccountAnalytics)
            .where(
                AccountAnalytics.account_id == account_id,
                AccountAnalytics.date >= start_date,
                AccountAnalytics.date <= end_date,
            )
            .order_by(AccountAnalytics.date)
        )
        return list(result.scalars())

    async def create_alert_rule(self, user_id: str, data: AlertRuleCreate) -> AlertRule:
        rule = AlertRule(
            owner_id=user_id,
            account_id=data.account_id,
            name=data.name,
            metric=data.metric,
            operator=data.operator,
            threshold=data.threshold,
            notification_channels=data.notification_channels,
        )
        self.db.add(rule)
        await self.db.flush()
        return rule
