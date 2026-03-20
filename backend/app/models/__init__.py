"""SQLAlchemy ORM models for the AI WeMedia platform."""
from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ──────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────────────────────────────────────

def _uuid() -> str:
    return str(uuid.uuid4())


# ──────────────────────────────────────────────────────────────────────────────
# Enumerations
# ──────────────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    OPERATOR = "operator"
    ANALYST = "analyst"
    VIEWER = "viewer"


class PlatformType(str, enum.Enum):
    WECHAT = "wechat"           # 公众号
    XIAOHONGSHU = "xiaohongshu" # 小红书
    DOUYIN = "douyin"           # 抖音
    SHIPIN = "shipin"           # 视频号
    KUAISHOU = "kuaishou"       # 快手
    BILIBILI = "bilibili"       # B站


class ContentType(str, enum.Enum):
    ARTICLE = "article"         # 图文长文
    SHORT_VIDEO = "short_video" # 短视频
    LIVE = "live"               # 直播
    IMAGE = "image"             # 图文
    AUDIO = "audio"             # 音频


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class TopicStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PublishStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    PAUSED = "paused"


class OrderStatus(str, enum.Enum):
    MATCHED = "matched"
    NEGOTIATING = "negotiating"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class AIProvider(str, enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    WENXIN = "wenxin"
    TONGYI = "tongyi"


# ──────────────────────────────────────────────────────────────────────────────
# User & Auth
# ──────────────────────────────────────────────────────────────────────────────

class User(Base):
    """Platform user (operator/creator)."""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(200))
    avatar_url: Mapped[str | None] = mapped_column(String(512))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.OPERATOR)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    preferences: Mapped[dict | None] = mapped_column(JSON)  # notification channels, UI prefs
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    accounts: Mapped[list[SocialAccount]] = relationship(back_populates="owner")
    contents: Mapped[list[Content]] = relationship(back_populates="creator")
    topics: Mapped[list[Topic]] = relationship(back_populates="creator")


class RefreshToken(Base):
    """Stored refresh tokens for JWT rotation."""
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ──────────────────────────────────────────────────────────────────────────────
# Social Media Accounts
# ──────────────────────────────────────────────────────────────────────────────

class SocialAccount(Base):
    """Connected social media account (e.g., 抖音账号, 小红书账号)."""
    __tablename__ = "social_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    platform: Mapped[PlatformType] = mapped_column(Enum(PlatformType), nullable=False)
    platform_uid: Mapped[str] = mapped_column(String(255), nullable=False)  # platform's user ID
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512))
    access_token: Mapped[str | None] = mapped_column(Text)  # encrypted
    refresh_token: Mapped[str | None] = mapped_column(Text)  # encrypted
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    followers_count: Mapped[int] = mapped_column(Integer, default=0)
    following_count: Mapped[int] = mapped_column(Integer, default=0)
    content_count: Mapped[int] = mapped_column(Integer, default=0)
    # AI-computed positioning data
    positioning: Mapped[dict | None] = mapped_column(JSON)   # {stage, domain, tags, ...}
    health_score: Mapped[float | None] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner: Mapped[User] = relationship(back_populates="accounts")
    analytics: Mapped[list[AccountAnalytics]] = relationship(back_populates="account")


# ──────────────────────────────────────────────────────────────────────────────
# Topic & Content Generation (Module 2.1)
# ──────────────────────────────────────────────────────────────────────────────

class Topic(Base):
    """A content topic from the intelligent topic engine."""
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(100))   # e.g. "百度指数", "抖音热点", "粉丝评论"
    tags: Mapped[list | None] = mapped_column(JSON)           # ["护肤", "平价", "成分"]
    # Scoring (0-100)
    heat_score: Mapped[float] = mapped_column(Float, default=0.0)        # 传播热度
    competition_score: Mapped[float] = mapped_column(Float, default=0.0) # 竞争度
    match_score: Mapped[float] = mapped_column(Float, default=0.0)       # 账号匹配度
    commercial_score: Mapped[float] = mapped_column(Float, default=0.0)  # 商业潜力
    composite_score: Mapped[float] = mapped_column(Float, default=0.0)   # 综合评分
    # Predictions
    predicted_views_min: Mapped[int | None] = mapped_column(Integer)
    predicted_views_max: Mapped[int | None] = mapped_column(Integer)
    predicted_engagement_rate: Mapped[float | None] = mapped_column(Float)
    status: Mapped[TopicStatus] = mapped_column(Enum(TopicStatus), default=TopicStatus.PENDING)
    scheduled_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped[User | None] = relationship(back_populates="topics")
    contents: Mapped[list[Content]] = relationship(back_populates="topic")


class Content(Base):
    """A piece of content created for a topic."""
    __tablename__ = "contents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    creator_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    topic_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("topics.id", ondelete="SET NULL"))
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str | None] = mapped_column(Text)
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType), default=ContentType.ARTICLE)
    platform: Mapped[PlatformType | None] = mapped_column(Enum(PlatformType))
    status: Mapped[ContentStatus] = mapped_column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    style: Mapped[str | None] = mapped_column(String(100))    # 干货 / 种草 / 情感 / 热点
    tags: Mapped[list | None] = mapped_column(JSON)
    ai_provider: Mapped[AIProvider | None] = mapped_column(Enum(AIProvider))
    # Quality scores
    originality_score: Mapped[float | None] = mapped_column(Float)
    readability_score: Mapped[float | None] = mapped_column(Float)
    compliance_score: Mapped[float | None] = mapped_column(Float)
    value_score: Mapped[float | None] = mapped_column(Float)
    # Platform variants
    platform_versions: Mapped[dict | None] = mapped_column(JSON)  # {platform: body_text}
    media_urls: Mapped[list | None] = mapped_column(JSON)          # attached images / videos
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped[User | None] = relationship(back_populates="contents")
    topic: Mapped[Topic | None] = relationship(back_populates="contents")
    publish_tasks: Mapped[list[PublishTask]] = relationship(back_populates="content")
    analytics: Mapped[list[ContentAnalytics]] = relationship(back_populates="content")


class Material(Base):
    """素材库 - uploaded images, videos, copywriting snippets."""
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    material_type: Mapped[str] = mapped_column(String(50))  # image / video / text / audio
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    tags: Mapped[list | None] = mapped_column(JSON)
    ai_labels: Mapped[dict | None] = mapped_column(JSON)   # AI-generated classification
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PromptTemplate(Base):
    """提示词模板库."""
    __tablename__ = "prompt_templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    scene: Mapped[str] = mapped_column(String(100))   # topic / content / review / ad
    template: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[list | None] = mapped_column(JSON)  # [{name, description, default}]
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    use_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_quality_score: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# ──────────────────────────────────────────────────────────────────────────────
# User Profile & Interaction (Module 2.2)
# ──────────────────────────────────────────────────────────────────────────────

class FanProfile(Base):
    """Aggregated fan profile (one per platform account + platform user)."""
    __tablename__ = "fan_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="CASCADE"))
    platform_user_id: Mapped[str] = mapped_column(String(255), nullable=False)  # fan's platform ID
    nickname: Mapped[str | None] = mapped_column(String(200))
    # Basic attributes
    age_range: Mapped[str | None] = mapped_column(String(20))   # "18-24"
    gender: Mapped[str | None] = mapped_column(String(10))
    region: Mapped[str | None] = mapped_column(String(100))
    # Computed labels & segmentation
    segment: Mapped[str] = mapped_column(String(50), default="general")  # core / potential / lost / general
    tags: Mapped[list | None] = mapped_column(JSON)
    behavior_data: Mapped[dict | None] = mapped_column(JSON)  # interaction_freq, last_active, ...
    interaction_count: Mapped[int] = mapped_column(Integer, default=0)
    conversion_count: Mapped[int] = mapped_column(Integer, default=0)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class InteractionTask(Base):
    """Automated interaction task (reply / dm / notification)."""
    __tablename__ = "interaction_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(50))  # keyword / schedule / event
    trigger_config: Mapped[dict | None] = mapped_column(JSON)
    action_type: Mapped[str] = mapped_column(String(50))   # reply / dm / push
    message_template: Mapped[str] = mapped_column(Text, nullable=False)
    target_segment: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    executed_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ──────────────────────────────────────────────────────────────────────────────
# Analytics & Decision (Module 2.3)
# ──────────────────────────────────────────────────────────────────────────────

class AccountAnalytics(Base):
    """Daily account-level analytics snapshot."""
    __tablename__ = "account_analytics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="CASCADE"), index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    followers: Mapped[int] = mapped_column(Integer, default=0)
    followers_net_change: Mapped[int] = mapped_column(Integer, default=0)
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    # Extended metrics
    extra: Mapped[dict | None] = mapped_column(JSON)

    account: Mapped[SocialAccount] = relationship(back_populates="analytics")


class ContentAnalytics(Base):
    """Per-content analytics (aggregated per day)."""
    __tablename__ = "content_analytics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    content_id: Mapped[str] = mapped_column(String(36), ForeignKey("contents.id", ondelete="CASCADE"), index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)

    content: Mapped[Content] = relationship(back_populates="analytics")


class AlertRule(Base):
    """User-defined data alert threshold rule."""
    __tablename__ = "alert_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    metric: Mapped[str] = mapped_column(String(100), nullable=False)  # followers_loss_rate, view_count, ...
    operator: Mapped[str] = mapped_column(String(10))   # >, <, >=, <=, ==
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    notification_channels: Mapped[list] = mapped_column(JSON, default=list)  # ["email", "wechat"]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ──────────────────────────────────────────────────────────────────────────────
# Cross-platform Distribution (Module 2.4)
# ──────────────────────────────────────────────────────────────────────────────

class PublishTask(Base):
    """Scheduled / executed publish task."""
    __tablename__ = "publish_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    content_id: Mapped[str] = mapped_column(String(36), ForeignKey("contents.id", ondelete="CASCADE"))
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="CASCADE"))
    platform: Mapped[PlatformType] = mapped_column(Enum(PlatformType), nullable=False)
    status: Mapped[PublishStatus] = mapped_column(Enum(PublishStatus), default=PublishStatus.SCHEDULED)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    platform_post_id: Mapped[str | None] = mapped_column(String(255))  # post ID returned by platform
    error_message: Mapped[str | None] = mapped_column(Text)
    celery_task_id: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    content: Mapped[Content] = relationship(back_populates="publish_tasks")


# ──────────────────────────────────────────────────────────────────────────────
# Commercial Monetization (Module 2.5)
# ──────────────────────────────────────────────────────────────────────────────

class CommercialOrder(Base):
    """Brand collaboration order (商单)."""
    __tablename__ = "commercial_orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="SET NULL"))
    brand_name: Mapped[str] = mapped_column(String(200), nullable=False)
    order_type: Mapped[str] = mapped_column(String(100))  # 种草 / 带货 / 广告 / 直播
    amount: Mapped[float | None] = mapped_column(Float)
    commission_rate: Mapped[float | None] = mapped_column(Float)  # %
    platform: Mapped[PlatformType | None] = mapped_column(Enum(PlatformType))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.MATCHED)
    requirements: Mapped[str | None] = mapped_column(Text)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    match_score: Mapped[float | None] = mapped_column(Float)  # AI match relevance 0-100
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class RevenueRecord(Base):
    """Revenue tracking record across all monetization channels."""
    __tablename__ = "revenue_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("social_accounts.id", ondelete="SET NULL"))
    channel: Mapped[str] = mapped_column(String(50))  # order / ecommerce / knowledge / private
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="CNY")
    description: Mapped[str | None] = mapped_column(String(500))
    reference_id: Mapped[str | None] = mapped_column(String(255))  # order_id / transaction_id
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ──────────────────────────────────────────────────────────────────────────────
# Workflow Automation (Section 4.3)
# ──────────────────────────────────────────────────────────────────────────────

class WorkflowRule(Base):
    """User-defined automation workflow rule."""
    __tablename__ = "workflow_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    trigger_type: Mapped[str] = mapped_column(String(50))  # event / schedule / threshold
    trigger_config: Mapped[dict] = mapped_column(JSON)
    action_type: Mapped[str] = mapped_column(String(50))   # send_dm / generate_report / publish
    action_config: Mapped[dict] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    executed_count: Mapped[int] = mapped_column(Integer, default=0)
    last_executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
