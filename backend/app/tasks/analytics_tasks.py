"""Background tasks: platform analytics sync and alert rule checks."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.analytics_tasks.sync_all_platform_analytics")
def sync_all_platform_analytics() -> dict:
    """Sync analytics data from all connected platform APIs."""
    try:
        return asyncio.run(_async_sync_analytics())
    except Exception:
        logger.exception("Analytics sync failed")
        return {"error": "sync failed"}


async def _async_sync_analytics() -> dict:
    """
    For each active social account, call the platform API adapter
    and upsert today's AccountAnalytics record.
    In production, each platform has its own OAuth adapter.
    """
    from app.database import AsyncSessionLocal
    from app.models import AccountAnalytics, SocialAccount
    from sqlalchemy import select

    synced = 0
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(SocialAccount).where(SocialAccount.is_active == True))  # noqa: E712
        accounts = list(result.scalars())
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        for account in accounts:
            # Real implementation calls: platform_adapter.get_daily_stats(account)
            # Here we upsert placeholder data
            existing = await db.execute(
                select(AccountAnalytics).where(
                    AccountAnalytics.account_id == account.id,
                    AccountAnalytics.date == today,
                )
            )
            if not existing.scalar_one_or_none():
                snapshot = AccountAnalytics(
                    account_id=account.id,
                    date=today,
                    followers=account.followers_count,
                )
                db.add(snapshot)
            synced += 1
        await db.commit()
    return {"synced": synced}


@celery_app.task(name="app.tasks.analytics_tasks.check_alert_rules")
def check_alert_rules() -> dict:
    """Evaluate all active alert rules and fire notifications if triggered."""
    try:
        return asyncio.run(_async_check_alerts())
    except Exception:
        logger.exception("Alert check failed")
        return {"error": "alert check failed"}


async def _async_check_alerts() -> dict:
    from app.database import AsyncSessionLocal
    from app.models import AlertRule, AccountAnalytics, SocialAccount
    from sqlalchemy import select
    import operator as op

    _ops = {">": op.gt, "<": op.lt, ">=": op.ge, "<=": op.le, "==": op.eq, "!=": op.ne}

    triggered = 0
    async with AsyncSessionLocal() as db:
        rules_result = await db.execute(
            select(AlertRule).where(AlertRule.is_active == True)  # noqa: E712
        )
        rules = list(rules_result.scalars())

        for rule in rules:
            # Fetch the most recent analytics value for the metric
            current_value = await _get_metric_value(db, rule)
            compare_fn = _ops.get(rule.operator, op.gt)
            if current_value is not None and compare_fn(current_value, rule.threshold):
                rule.last_triggered_at = datetime.now(timezone.utc)
                triggered += 1
                # In production: send notification via email/SMS/WeChat
                logger.info("Alert triggered: %s (value=%.2f, threshold=%.2f)", rule.name, current_value, rule.threshold)
        await db.commit()
    return {"triggered": triggered, "checked": len(rules)}


async def _get_metric_value(db, rule: "AlertRule") -> float | None:  # type: ignore[name-defined]
    """Map alert rule metric name to a DB query value."""
    from app.models import AccountAnalytics
    from sqlalchemy import select

    metric_map = {
        "followers": "followers",
        "followers_loss_rate": None,
        "views": "views",
        "likes": "likes",
    }
    if rule.account_id and rule.metric in ("followers", "views", "likes", "comments"):
        col = getattr(AccountAnalytics, rule.metric, None)
        if col is None:
            return None
        result = await db.execute(
            select(col)
            .where(AccountAnalytics.account_id == rule.account_id)
            .order_by(AccountAnalytics.date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    return None
