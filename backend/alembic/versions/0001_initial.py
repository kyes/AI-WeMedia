"""Initial schema — all tables.

Revision ID: 0001
Revises: 
Create Date: 2026-03-20
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(200)),
        sa.Column("avatar_url", sa.String(512)),
        sa.Column("role", sa.Enum("admin","editor","operator","analyst","viewer", name="userrole"), nullable=False, server_default="operator"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("preferences", sa.JSON),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])

    # Refresh tokens
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Social accounts
    op.create_table(
        "social_accounts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Enum("wechat","xiaohongshu","douyin","shipin","kuaishou","bilibili", name="platformtype"), nullable=False),
        sa.Column("platform_uid", sa.String(255), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("avatar_url", sa.String(512)),
        sa.Column("access_token", sa.Text),
        sa.Column("refresh_token", sa.Text),
        sa.Column("token_expires_at", sa.DateTime(timezone=True)),
        sa.Column("followers_count", sa.Integer, server_default="0"),
        sa.Column("following_count", sa.Integer, server_default="0"),
        sa.Column("content_count", sa.Integer, server_default="0"),
        sa.Column("positioning", sa.JSON),
        sa.Column("health_score", sa.Float),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Topics
    op.create_table(
        "topics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("creator_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="SET NULL")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("source", sa.String(100)),
        sa.Column("tags", sa.JSON),
        sa.Column("heat_score", sa.Float, server_default="0"),
        sa.Column("competition_score", sa.Float, server_default="0"),
        sa.Column("match_score", sa.Float, server_default="0"),
        sa.Column("commercial_score", sa.Float, server_default="0"),
        sa.Column("composite_score", sa.Float, server_default="0"),
        sa.Column("predicted_views_min", sa.Integer),
        sa.Column("predicted_views_max", sa.Integer),
        sa.Column("predicted_engagement_rate", sa.Float),
        sa.Column("status", sa.Enum("pending","confirmed","in_progress","completed","cancelled", name="topicstatus"), server_default="pending"),
        sa.Column("scheduled_date", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Contents
    op.create_table(
        "contents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("creator_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("topic_id", sa.String(36), sa.ForeignKey("topics.id", ondelete="SET NULL")),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="SET NULL")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("body", sa.Text),
        sa.Column("content_type", sa.Enum("article","short_video","live","image","audio", name="contenttype"), server_default="article"),
        sa.Column("platform", sa.Enum("wechat","xiaohongshu","douyin","shipin","kuaishou","bilibili", name="platformtype2")),
        sa.Column("status", sa.Enum("draft","in_review","approved","published","rejected","archived", name="contentstatus"), server_default="draft"),
        sa.Column("style", sa.String(100)),
        sa.Column("tags", sa.JSON),
        sa.Column("ai_provider", sa.Enum("openai","anthropic","wenxin","tongyi", name="aiprovider")),
        sa.Column("originality_score", sa.Float),
        sa.Column("readability_score", sa.Float),
        sa.Column("compliance_score", sa.Float),
        sa.Column("value_score", sa.Float),
        sa.Column("platform_versions", sa.JSON),
        sa.Column("media_urls", sa.JSON),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Materials
    op.create_table(
        "materials",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("material_type", sa.String(50)),
        sa.Column("url", sa.String(512), nullable=False),
        sa.Column("tags", sa.JSON),
        sa.Column("ai_labels", sa.JSON),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Prompt templates
    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("scene", sa.String(100)),
        sa.Column("template", sa.Text, nullable=False),
        sa.Column("variables", sa.JSON),
        sa.Column("is_builtin", sa.Boolean, server_default="false"),
        sa.Column("is_public", sa.Boolean, server_default="false"),
        sa.Column("use_count", sa.Integer, server_default="0"),
        sa.Column("avg_quality_score", sa.Float),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Fan profiles
    op.create_table(
        "fan_profiles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform_user_id", sa.String(255), nullable=False),
        sa.Column("nickname", sa.String(200)),
        sa.Column("age_range", sa.String(20)),
        sa.Column("gender", sa.String(10)),
        sa.Column("region", sa.String(100)),
        sa.Column("segment", sa.String(50), server_default="general"),
        sa.Column("tags", sa.JSON),
        sa.Column("behavior_data", sa.JSON),
        sa.Column("interaction_count", sa.Integer, server_default="0"),
        sa.Column("conversion_count", sa.Integer, server_default="0"),
        sa.Column("last_active_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Interaction tasks
    op.create_table(
        "interaction_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("trigger_type", sa.String(50)),
        sa.Column("trigger_config", sa.JSON),
        sa.Column("action_type", sa.String(50)),
        sa.Column("message_template", sa.Text, nullable=False),
        sa.Column("target_segment", sa.String(50)),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("executed_count", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Account analytics
    op.create_table(
        "account_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("followers", sa.Integer, server_default="0"),
        sa.Column("followers_net_change", sa.Integer, server_default="0"),
        sa.Column("views", sa.Integer, server_default="0"),
        sa.Column("likes", sa.Integer, server_default="0"),
        sa.Column("comments", sa.Integer, server_default="0"),
        sa.Column("shares", sa.Integer, server_default="0"),
        sa.Column("revenue", sa.Float, server_default="0"),
        sa.Column("extra", sa.JSON),
    )

    # Content analytics
    op.create_table(
        "content_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("content_id", sa.String(36), sa.ForeignKey("contents.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("views", sa.Integer, server_default="0"),
        sa.Column("likes", sa.Integer, server_default="0"),
        sa.Column("comments", sa.Integer, server_default="0"),
        sa.Column("shares", sa.Integer, server_default="0"),
        sa.Column("conversions", sa.Integer, server_default="0"),
        sa.Column("revenue", sa.Float, server_default="0"),
    )

    # Alert rules
    op.create_table(
        "alert_rules",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("metric", sa.String(100), nullable=False),
        sa.Column("operator", sa.String(10)),
        sa.Column("threshold", sa.Float, nullable=False),
        sa.Column("notification_channels", sa.JSON),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("last_triggered_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Publish tasks
    op.create_table(
        "publish_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("content_id", sa.String(36), sa.ForeignKey("contents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.Enum("wechat","xiaohongshu","douyin","shipin","kuaishou","bilibili", name="platformtype3"), nullable=False),
        sa.Column("status", sa.Enum("scheduled","publishing","published","failed","paused", name="publishstatus"), server_default="scheduled"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("platform_post_id", sa.String(255)),
        sa.Column("error_message", sa.Text),
        sa.Column("celery_task_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Commercial orders
    op.create_table(
        "commercial_orders",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="SET NULL")),
        sa.Column("brand_name", sa.String(200), nullable=False),
        sa.Column("order_type", sa.String(100)),
        sa.Column("amount", sa.Float),
        sa.Column("commission_rate", sa.Float),
        sa.Column("platform", sa.Enum("wechat","xiaohongshu","douyin","shipin","kuaishou","bilibili", name="platformtype4")),
        sa.Column("status", sa.Enum("matched","negotiating","in_progress","completed","rejected", name="orderstatus"), server_default="matched"),
        sa.Column("requirements", sa.Text),
        sa.Column("deadline", sa.DateTime(timezone=True)),
        sa.Column("match_score", sa.Float),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Revenue records
    op.create_table(
        "revenue_records",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(36), sa.ForeignKey("social_accounts.id", ondelete="SET NULL")),
        sa.Column("channel", sa.String(50)),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("currency", sa.String(10), server_default="CNY"),
        sa.Column("description", sa.String(500)),
        sa.Column("reference_id", sa.String(255)),
        sa.Column("earned_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Workflow rules
    op.create_table(
        "workflow_rules",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("trigger_type", sa.String(50)),
        sa.Column("trigger_config", sa.JSON),
        sa.Column("action_type", sa.String(50)),
        sa.Column("action_config", sa.JSON),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("executed_count", sa.Integer, server_default="0"),
        sa.Column("last_executed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    tables = [
        "workflow_rules", "revenue_records", "commercial_orders", "publish_tasks",
        "alert_rules", "content_analytics", "account_analytics", "interaction_tasks",
        "fan_profiles", "prompt_templates", "materials", "contents", "topics",
        "social_accounts", "refresh_tokens", "users",
    ]
    for table in tables:
        op.drop_table(table)
