"""API v1 router — aggregates all sub-routers."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import (
    accounts,
    ai_support,
    analytics,
    auth,
    content,
    distribution,
    interaction,
    monetization,
    topics,
    workflows,
)

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(accounts.router)
router.include_router(topics.router)
router.include_router(content.router)
router.include_router(analytics.router)
router.include_router(distribution.router)
router.include_router(monetization.router)
router.include_router(interaction.router)
router.include_router(ai_support.router)
router.include_router(workflows.router)
