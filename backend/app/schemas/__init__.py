"""Pydantic schemas for request/response validation."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import (
    AIProvider,
    ContentStatus,
    ContentType,
    OrderStatus,
    PlatformType,
    PublishStatus,
    TopicStatus,
    UserRole,
)


# ──────────────────────────────────────────────────────────────────────────────
# Shared base
# ──────────────────────────────────────────────────────────────────────────────

class OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────────────────────────────────────
# Auth / User
# ──────────────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    refresh_token: str


class UserOut(OrmBase):
    id: str
    email: str
    username: str
    full_name: str | None
    avatar_url: str | None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    avatar_url: str | None = None
    preferences: dict | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


# ──────────────────────────────────────────────────────────────────────────────
# Social Accounts
# ──────────────────────────────────────────────────────────────────────────────

class SocialAccountOut(OrmBase):
    id: str
    platform: PlatformType
    name: str
    avatar_url: str | None
    followers_count: int
    content_count: int
    positioning: dict | None
    health_score: float | None
    is_active: bool
    created_at: datetime


class AccountPositioningUpdate(BaseModel):
    stage: str | None = None      # 冷启动 / 成长 / 成熟 / 衰退
    domain: str | None = None     # "美妆→敏感肌护肤→平价好物"
    tags: list[str] | None = None
    strategy: str | None = None


# ──────────────────────────────────────────────────────────────────────────────
# Topics
# ──────────────────────────────────────────────────────────────────────────────

class TopicCreate(BaseModel):
    title: str = Field(..., max_length=500)
    description: str | None = None
    tags: list[str] | None = None
    account_id: str | None = None
    scheduled_date: datetime | None = None


class TopicOut(OrmBase):
    id: str
    title: str
    description: str | None
    source: str | None
    tags: list | None
    heat_score: float
    competition_score: float
    match_score: float
    commercial_score: float
    composite_score: float
    predicted_views_min: int | None
    predicted_views_max: int | None
    predicted_engagement_rate: float | None
    status: TopicStatus
    scheduled_date: datetime | None
    created_at: datetime


class TopicGenerateRequest(BaseModel):
    """Request body for AI-driven topic generation."""
    account_id: str
    count: int = Field(5, ge=1, le=20)
    sources: list[str] = Field(default_factory=lambda: ["hot_search", "fan_comments", "industry"])
    custom_keywords: list[str] | None = None


class TopicScoreRequest(BaseModel):
    topic_id: str
    account_id: str


# ──────────────────────────────────────────────────────────────────────────────
# Content Generation
# ──────────────────────────────────────────────────────────────────────────────

class ContentGenerateRequest(BaseModel):
    """Request body for AI content generation."""
    topic_id: str | None = None
    custom_topic: str | None = None
    platform: PlatformType
    content_type: ContentType = ContentType.ARTICLE
    style: str = "专业干货"   # 专业干货 / 轻松幽默 / 情感共鸣 / 种草安利
    word_count: int = Field(1200, ge=100, le=5000)
    ai_provider: AIProvider | None = None
    account_id: str | None = None

    @field_validator("custom_topic", "topic_id")
    @classmethod
    def require_topic(cls, v: Any, info: Any) -> Any:
        return v


class ContentCreate(BaseModel):
    title: str = Field(..., max_length=500)
    body: str | None = None
    content_type: ContentType = ContentType.ARTICLE
    platform: PlatformType | None = None
    style: str | None = None
    tags: list[str] | None = None
    topic_id: str | None = None
    account_id: str | None = None


class ContentUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    status: ContentStatus | None = None
    tags: list[str] | None = None


class ContentOut(OrmBase):
    id: str
    title: str
    body: str | None
    content_type: ContentType
    platform: PlatformType | None
    status: ContentStatus
    style: str | None
    tags: list | None
    ai_provider: AIProvider | None
    originality_score: float | None
    readability_score: float | None
    compliance_score: float | None
    value_score: float | None
    platform_versions: dict | None
    created_at: datetime
    updated_at: datetime


class ContentAdaptRequest(BaseModel):
    """Adapt one piece of content to multiple platforms."""
    content_id: str
    target_platforms: list[PlatformType]


# ──────────────────────────────────────────────────────────────────────────────
# Analytics
# ──────────────────────────────────────────────────────────────────────────────

class AccountAnalyticsOut(OrmBase):
    id: str
    account_id: str
    date: datetime
    followers: int
    followers_net_change: int
    views: int
    likes: int
    comments: int
    shares: int
    revenue: float


class DashboardSummary(BaseModel):
    """Aggregated dashboard data."""
    total_followers: int
    weekly_views: int
    weekly_interactions: int
    monthly_revenue: float
    health_score: float
    platform_breakdown: list[dict]
    growth_trend: list[dict]  # [{date, followers, views, interactions}]
    top_content: list[dict]
    alerts: list[dict]


class AlertRuleCreate(BaseModel):
    name: str = Field(..., max_length=200)
    account_id: str | None = None
    metric: str
    operator: str = Field(..., pattern=r"^(>|<|>=|<=|==|!=)$")
    threshold: float
    notification_channels: list[str] = Field(default_factory=list)


class AlertRuleOut(OrmBase):
    id: str
    name: str
    metric: str
    operator: str
    threshold: float
    notification_channels: list
    is_active: bool
    last_triggered_at: datetime | None
    created_at: datetime


# ──────────────────────────────────────────────────────────────────────────────
# Distribution / Publishing
# ──────────────────────────────────────────────────────────────────────────────

class PublishTaskCreate(BaseModel):
    content_id: str
    account_id: str
    platform: PlatformType
    scheduled_at: datetime


class PublishTaskOut(OrmBase):
    id: str
    content_id: str
    account_id: str
    platform: PlatformType
    status: PublishStatus
    scheduled_at: datetime
    published_at: datetime | None
    platform_post_id: str | None
    error_message: str | None
    created_at: datetime


class BestPublishTimeRequest(BaseModel):
    account_id: str
    platform: PlatformType


class BestPublishTimeResponse(BaseModel):
    platform: PlatformType
    recommended_times: list[str]  # ["08:00", "20:00"]
    heat_scores: list[float]


# ──────────────────────────────────────────────────────────────────────────────
# Monetization
# ──────────────────────────────────────────────────────────────────────────────

class CommercialOrderCreate(BaseModel):
    brand_name: str = Field(..., max_length=200)
    order_type: str
    amount: float | None = None
    commission_rate: float | None = None
    platform: PlatformType | None = None
    requirements: str | None = None
    deadline: datetime | None = None
    account_id: str | None = None


class CommercialOrderUpdate(BaseModel):
    status: OrderStatus | None = None
    requirements: str | None = None
    deadline: datetime | None = None


class CommercialOrderOut(OrmBase):
    id: str
    brand_name: str
    order_type: str
    amount: float | None
    commission_rate: float | None
    platform: PlatformType | None
    status: OrderStatus
    deadline: datetime | None
    match_score: float | None
    created_at: datetime


class RevenueSummary(BaseModel):
    total: float
    by_channel: dict[str, float]
    monthly_trend: list[dict]


# ──────────────────────────────────────────────────────────────────────────────
# AI & Prompt Templates
# ──────────────────────────────────────────────────────────────────────────────

class PromptTemplateCreate(BaseModel):
    name: str = Field(..., max_length=200)
    scene: str
    template: str
    variables: list[dict] | None = None
    is_public: bool = False


class PromptTemplateOut(OrmBase):
    id: str
    name: str
    scene: str
    template: str
    variables: list | None
    is_builtin: bool
    is_public: bool
    use_count: int
    avg_quality_score: float | None
    created_at: datetime


class AIGenerateRequest(BaseModel):
    prompt: str
    provider: AIProvider | None = None
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(2000, ge=100, le=8000)
    system_prompt: str | None = None


class AIGenerateResponse(BaseModel):
    content: str
    provider: AIProvider
    model: str
    tokens_used: int
    latency_ms: int


# ──────────────────────────────────────────────────────────────────────────────
# Workflow Automation
# ──────────────────────────────────────────────────────────────────────────────

class WorkflowRuleCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: str | None = None
    trigger_type: str  # event / schedule / threshold
    trigger_config: dict
    action_type: str
    action_config: dict


class WorkflowRuleOut(OrmBase):
    id: str
    name: str
    description: str | None
    trigger_type: str
    trigger_config: dict
    action_type: str
    action_config: dict
    is_active: bool
    executed_count: int
    last_executed_at: datetime | None
    created_at: datetime


# ──────────────────────────────────────────────────────────────────────────────
# Fan profiles / Interaction
# ──────────────────────────────────────────────────────────────────────────────

class FanProfileOut(OrmBase):
    id: str
    account_id: str
    platform_user_id: str
    nickname: str | None
    age_range: str | None
    gender: str | None
    region: str | None
    segment: str
    tags: list | None
    interaction_count: int
    last_active_at: datetime | None


class InteractionTaskCreate(BaseModel):
    name: str = Field(..., max_length=200)
    account_id: str
    trigger_type: str  # keyword / schedule / event
    trigger_config: dict
    action_type: str   # reply / dm / push
    message_template: str
    target_segment: str | None = None


class InteractionTaskOut(OrmBase):
    id: str
    name: str
    account_id: str
    trigger_type: str
    trigger_config: dict | None
    action_type: str
    message_template: str
    target_segment: str | None
    is_active: bool
    executed_count: int
    created_at: datetime


# ──────────────────────────────────────────────────────────────────────────────
# Generic helpers
# ──────────────────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    pages: int


class MessageResponse(BaseModel):
    message: str

    @classmethod
    def ok(cls, msg: str = "ok") -> "MessageResponse":
        return cls(message=msg)
